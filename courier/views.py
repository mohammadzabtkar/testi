from .serializers import CompleteCourierProfileSerializer
from rest_framework import status
from task.models import Task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import  Courier
from task.models import Task

class CompleteCourierProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ ایجاد پروفایل پیک (در صورت عدم وجود) """
        serializer = CompleteCourierProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "پروفایل پیک با موفقیت ثبت شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """ بروزرسانی پروفایل پیک (در صورت وجود) """
        try:
            courier_profile = Courier.objects.get(user=request.user)
            serializer = CompleteCourierProfileSerializer(courier_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "پروفایل پیک با موفقیت بروزرسانی شد."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Courier.DoesNotExist:
            return Response({"error": "پروفایل پیک یافت نشد. ابتدا با متد POST ثبت کنید."}, status=status.HTTP_404_NOT_FOUND)


class UpdateCourierStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_status = request.data.get("status")
        try:
            courier = Courier.objects.get(user=request.user)
        except Courier.DoesNotExist:
            return Response({"error": "پروفایل پیک یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
        courier_online_tasks_count = Task.objects.filter(courier = courier , status="accepted").count()
        print(courier_online_tasks_count)
        print("PPPPPPPP")

        if new_status not in ["online", "offline", "at_work"]:
            return Response({"error": "وضعیت نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)
        elif new_status == "offline" and courier_online_tasks_count > 0 :
            return Response({"error": "پیک یک بسته تحویل داده نشده دارد"})
        elif new_status == "offline" and courier_online_tasks_count == 0 :
            # ذخیره وضعیت جدید
            courier.status = new_status
            courier.save()

            # دریافت لایه کانال
            channel_layer = get_channel_layer()
            print(channel_layer)
            group_name = f"public_group_{courier.vehicle_type}"
            print(group_name)

            # ارسال پیام به گروه
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "courier_chat_message",
                    "action": "courier_is_online",
                    "message": f"پیک {courier.user.username} وضعیت خود را به {new_status} تغییر داد.",
                    "courier_id": courier.id,
                    "status": new_status,
                },
            )

            return Response({"message": f"وضعیت شما به '{new_status}' تغییر کرد."}, status=status.HTTP_200_OK)



class AcceptTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        user = request.user

        # دریافت پیک
        courier = get_object_or_404(Courier, user=user, status="online")

        # دریافت تسک
        task = get_object_or_404(Task, id=task_id, status="pending")

        # تغییر وضعیت پیک به at_work
        courier.status = "at_work"
        courier.save()

        # تغییر وضعیت تسک به accepted
        task.status = "accepted"
        task.courier = courier
        task.save()

        # دریافت اطلاعات گروه‌ها
        vehicle_type = courier.vehicle_type
        public_group = f"public_group_{vehicle_type}"
        private_group = f"private_group_{task.id}_{vehicle_type}"

        # ارسال پیام به WebSocket برای خروج از گروه عمومی و ورود به گروه خصوصی
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            public_group,
            {
                "type": "chat.message",
                "action": "leave_group",
                "courier_id": courier.id,
                "task_id": task.id,
                "message": f"Courier {courier.id} accepted Task {task.id} and left public group.",
            },
        )

        async_to_sync(channel_layer.group_send)(
            private_group,
            {
                "type": "chat.message",
                "action": "join_group",
                "courier_id": courier.id,
                "task_id": task.id,
                "message": f"Courier {courier.id} joined private group for Task {task.id}.",
            },
        )

        return Response({"message": "Task accepted successfully.", "task_id": task.id, "courier_id": courier.id})
