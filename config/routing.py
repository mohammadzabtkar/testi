from django.urls import path
# from task.consumers import TaskConsumer, CourierConsumer
from task.consumers import Task_Group_Select

websocket_urlpatterns = [
    # path('ws/courier/', CourierConsumer.as_asgi()),  # برای مدیریت وضعیت پیک‌ها
    path('ws/sender_goto_public_group/', Task_Group_Select.as_asgi()),  # برای مدیریت تسک‌ها توسط مشتری
    path('ws/courier_goto_public_group/', Task_Group_Select.as_asgi()),
]
