from django.urls import path
# from task.consumers import TaskConsumer, CourierConsumer
from task.consumers import Group_Selecter_Consumer

websocket_urlpatterns = [
    # path('ws/courier/', CourierConsumer.as_asgi()),  # برای مدیریت وضعیت پیک‌ها
    path('ws/sender_goto_public_group/', Group_Selecter_Consumer.as_asgi()),  # برای مدیریت تسک‌ها توسط مشتری
    path('ws/courier_goto_public_group/', Group_Selecter_Consumer.as_asgi()),
]
