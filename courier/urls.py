from django.urls import path
from .views import CompleteCourierProfileView ,UpdateCourierStatusView

urlpatterns = [
    path('complete-profile/', CompleteCourierProfileView.as_view(), name='api-complete-courier-profile'),
    path('update_status/', UpdateCourierStatusView.as_view(), name='api-update-courier-status'),
]
