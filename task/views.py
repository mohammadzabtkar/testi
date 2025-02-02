
# views.py
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Task
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync

class TaskCreationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user

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
            # ارسال پیام به WebSocket برای تسک جدید
            channel_layer = get_channel_layer()
            message = {
                "type": "send_task_update",
                "task_id": task.id,
                # اضافه کردن وضعیت یا سایر اطلاعات
            }

            # ارسال پیام به گروه WebSocket
            async_to_sync(channel_layer.group_send)(
                f"task_{task.id}",  # گروه WebSocket برای این تسک
                {
                    "type": "send_task_update",  # نوع پیام (باید در TaskConsumer تعریف شود)
                    "message": json.dumps(message),  # پیام واقعی که می‌خواهید ارسال کنید
                }
            )


            return Response({"message": "Task created successfully", "task_id": task.id},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
