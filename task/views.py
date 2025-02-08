# views.py
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class TaskCreationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        print("Request data:", data)  # پرینت داده‌های ورودی درخواست

        if user.groups.filter(name='senders').exists():
            print("User is a sender.")  # پرینت وقتی که کاربر عضو گروه 'senders' باشد

            try:
                task = Task.objects.create(
                    sender=user,
                    status=data.get("status", "pending"),
                    distance_km=16,  # بعدا محاسبه می‌شود
                    package_note=data.get("package_note"),
                    package_category=data.get("package_category", "other"),
                    source_address=data.get("source_address"),
                    vehicle_type=data.get("vehicle_type"),
                    destination_user_name=data.get("destination_user_name"),
                    destination_address=data.get("destination_address"),
                    destination_address_latitude=data.get("destination_address_latitude"),
                    destination_address_longitude=data.get("destination_address_longitude"),
                    estimated_price=data.get("estimated_price"),
                    payment_side=data.get("payment_side", "prepay"),
                    source_address_latitude=data.get("source_address_latitude"),
                    source_address_longitude=data.get("source_address_longitude"),
                )
                print("$$$$$$$$$$$")
                print(task)
                print(f"Task created successfully with ID: {task.id}")  # پرینت ID تسک پس از ایجاد

                # ارسال پیام به WebSocket
                self.send_task_to_channel(task, action='new_task')

                return Response({"message": "Task created successfully", "task_id": task.id},
                                status=status.HTTP_201_CREATED)

            except Exception as e:
                print(f"Error creating task: {e}")  # پرینت خطا در صورت بروز
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("User is not authorized to create tasks.")  # پرینت زمانی که کاربر اجازه ایجاد تسک ندارد
            return Response({"message": "User is not authorized to create tasks."},
                            status=status.HTTP_403_FORBIDDEN)

    def send_task_to_channel(self, task, action):
        print(f"Sending task {action} message to WebSocket...")  # پرینت قبل از ارسال پیام
        channel_layer = get_channel_layer()
        public_group_name = f"public_group_{task.vehicle_type}"
        print(public_group_name)

        message = {
            'type': 'sender_chat_message',
            'action': action,
            'message': f'تسک {action} برای {task.vehicle_type}!',
            'task_id': task.id,
            'sender': task.sender.username,
            'status': task.status,
            'source_address': task.source_address,
            'destination_address': task.destination_address,
        }

        async_to_sync(channel_layer.group_send)(public_group_name, message)
        print("Message sent to channel!")  # پرینت بعد از ارسال پیام


class TaskCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        user = request.user

        try:
            task = Task.objects.get(id=task_id, sender=user)

            if task.status in ['pending', 'assigned']:  # فقط وقتی تسک در این وضعیت‌هاست، لغو میشه
                task.status = 'canceled'
                task.save()

                # ارسال پیام لغو به WebSocket
                self.send_task_cancellation_to_channel(task)

                return Response({"message": "Task canceled successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Task cannot be canceled in its current state."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({"error": "Task not found or you are not authorized to cancel it."},
                            status=status.HTTP_404_NOT_FOUND)

    def send_task_cancellation_to_channel(self, task):
        channel_layer = get_channel_layer()
        public_group_name = f"public_group_{task.vehicle_type}"

        async_to_sync(channel_layer.group_send)(
            public_group_name,
            {
                'type': 'chat_message',
                'action': 'canceled',
                'message': f'تسک با شناسه {task.id} لغو شد!',
                'task_id': task.id,
            }
        )
