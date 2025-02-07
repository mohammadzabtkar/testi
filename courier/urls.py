from django.urls import path
from .views import CompleteCourierProfileView

urlpatterns = [
    path('complete-profile/', CompleteCourierProfileView.as_view(), name='api-complete-courier-profile'),
]
