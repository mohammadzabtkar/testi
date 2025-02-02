import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

# تنظیم متغیر محیطی برای مشخص کردن تنظیمات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# راه‌اندازی Django
django.setup()
from task.routing import websocket_urlpatterns as task_websocket_urlpatterns

# تعریف روتینگ برای WebSocket
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            task_websocket_urlpatterns
        )
    ),
})

