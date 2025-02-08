from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Courier
from .serializers import CompleteCourierProfileSerializer
from task.consumers import Group_Selecter_Consumer

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



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Courier
from task.models import Task

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
