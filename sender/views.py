
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import SenderAddress
from .serializers import CompleteSenderProfileSerializer

class SenderProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ ایجاد پروفایل برای سندر (در صورت عدم وجود) """
        serializer = CompleteSenderProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "پروفایل سندر با موفقیت ثبت شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """ بروزرسانی پروفایل سندر (در صورت وجود) """
        try:
            sender_profile = SenderAddress.objects.get(user=request.user)
            serializer = CompleteSenderProfileSerializer(sender_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "پروفایل سندر با موفقیت بروزرسانی شد."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SenderAddress.DoesNotExist:
            return Response({"error": "پروفایل سندر یافت نشد. ابتدا با متد POST ثبت کنید."}, status=status.HTTP_404_NOT_FOUND)
