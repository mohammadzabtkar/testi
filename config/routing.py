from django.urls import path
# from task.consumers import TaskConsumer, CourierConsumer
from task.consumers import Group_Selecter_Consumer

websocket_urlpatterns = [
    # path('ws/courier/', CourierConsumer.as_asgi()),  # برای مدیریت وضعیت پیک‌ها
    path('ws/public_group_selector/', Group_Selecter_Consumer.as_asgi()),








    # path('ws/courier_goto_public_group/', Group_Selecter_Consumer.as_asgi()),
]
