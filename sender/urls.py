from django.urls import path
from .views import SenderProfileView

urlpatterns = [
    path('complete-profile/', SenderProfileView.as_view(), name='api-complete-sender-profile'),
]
