# routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/task/$', consumers.TaskConsumer.as_asgi()),  # پیام‌های عمومی
    re_path(r'ws/task/(?P<task_id>\d+)/$', consumers.TaskConsumer.as_asgi()),  # پیام‌های مربوط به یک تسک خاص
    re_path(r'ws/task/(?P<task_id>\d+)/$', consumers.TaskConsumer.as_asgi()),

]
