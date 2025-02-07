from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Courier
from .serializers import CompleteCourierProfileSerializer

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
