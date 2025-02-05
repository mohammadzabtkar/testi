from django.urls import path
from task.consumers import TaskConsumer, CourierConsumer

websocket_urlpatterns = [
    path('ws/public_task/', TaskConsumer.as_asgi()),  # برای مدیریت تسک‌ها توسط مشتری
    path('ws/courier/', CourierConsumer.as_asgi()),        # برای مدیریت وضعیت پیک‌ها
    path('ws/public_courier/', TaskConsumer.as_asgi()),
]
