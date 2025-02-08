from django.urls import path
from .views import CompleteCourierProfileView ,UpdateCourierStatusView , AcceptTaskAPIView

urlpatterns = [
    path('complete-profile/', CompleteCourierProfileView.as_view(), name='api-complete-courier-profile'),
    path('update_status/', UpdateCourierStatusView.as_view(), name='api-update-courier-status'),
    path('accept_task/', AcceptTaskAPIView.as_view(), name='accept-task'),
]
