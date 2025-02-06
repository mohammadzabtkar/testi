from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
import urllib.parse
import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from task.models import Task
from courier.models import Courier


class BaseConsumer(AsyncWebsocketConsumer):
    async def get_user_from_token(self, token_key):
        try:
            validated_token = JWTAuthentication().get_validated_token(token_key)
            user = await database_sync_to_async(JWTAuthentication().get_user)(validated_token)
            return user
        except (InvalidToken, TokenError):
            return AnonymousUser()

    async def get_user_group(self):
        if await database_sync_to_async(self.user.groups.filter(name='senders').exists)():
            return "senders"
        elif await database_sync_to_async(self.user.groups.filter(name='couriers').exists)():
            return "couriers"
        return None

    async def get_token(self):
        query_string = self.scope['query_string'].decode()
        query_params = urllib.parse.parse_qs(query_string)
        return query_params.get('token', [None])[0]

    async def get_authenticated_user(self):
        token_key = await self.get_token()
        if not token_key:
            return None
        user = await self.get_user_from_token(token_key)
        return user if user and not isinstance(user, AnonymousUser) else None


class Task_Group_Select(BaseConsumer):
    async def connect(self):
        print("WebSocket connection attempt...")
        self.user = await self.get_authenticated_user()

        if not self.user:
            print("User is not authorized.")
            await self.close()
            return

        user_group = await self.get_user_group()

        if user_group == "senders":
            await self.handle_sender()
        elif user_group == "couriers":
            await self.handle_courier()
        else:
            print("User group not recognized.")
            await self.close()

    async def handle_sender(self):
        """مدیریت ورود فرستنده و انتخاب گروه عمومی بر اساس تسک‌های باز"""
        print("User is a sender ...")
        try:
            task = await database_sync_to_async(Task.objects.filter(status="pending").order_by('-id').first)()
            if not task:
                print("No pending tasks found.")
                await self.close()
                return

            vehicle_type = task.vehicle_type
            self.room_group_name = f"public_group_{vehicle_type}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        except Exception as e:
            print(f"An error occurred: {e}")
            await self.close()

    async def handle_courier(self):
        """مدیریت ورود پیک و تخصیص گروه عمومی بر اساس وسیله نقلیه"""
        print("User is a courier ...")
        try:
            courier = await database_sync_to_async(Courier.objects.get)(user=self.user)
            if courier.status == "online":
                vehicle_type = courier.vehicle_type
                self.room_group_name = f"public_group_{vehicle_type}"
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.accept()
            elif courier.status in ["offline", "at_work"]:
                print(f"Courier is {courier.status}. Closing connection.")
                await self.close()
        except Courier.DoesNotExist:
            print("Courier does not exist.")
            await self.close()
        except Exception as e:
            print(f"An error occurred: {e}")
            await self.close()

    async def disconnect(self, close_code):
        print("User disconnected...")
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'action': event['action'],
            'message': event['message'],
            'task_id': event['task_id'],
            'sender': event['sender'],
            'status': event['status'],
            'source_address': event['source_address'],
            'destination_address': event['destination_address'],
        }))
        print(f"Message received in consumer: {event['message']}")


# class CourierConsumer(BaseConsumer):
#     async def connect(self):
#         # دریافت کاربر احراز هویت شده
#         self.user = await self.get_authenticated_user()
#
#         # اگر کاربر احراز هویت نشده باشد یا پیک نباشد، اتصال قطع می‌شود
#         if not self.user:
#             await self.close()
#         else:
#             vehicle_type = await self.get_vehicle_type()  # دریافت نوع وسیله نقلیه
#             self.vehicle_group = f"vehicle_{vehicle_type}"  # نام گروه بر اساس نوع وسیله نقلیه
#             await self.channel_layer.group_add(self.vehicle_group, self.channel_name)
#             await self.accept()
#
#     # دریافت نوع وسیله نقلیه پیک
#     @database_sync_to_async
#     def get_vehicle_type(self):
#         courier = Courier.objects.get(user=self.user)
#         return courier.vehicle_type
#
#     # قطع اتصال از کانال
#     async def disconnect(self, close_code):
#         if hasattr(self, 'vehicle_group'):
#             await self.channel_layer.group_discard(self.vehicle_group, self.channel_name)
#
#     # دریافت داده‌ها از کلاینت
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         if data.get('action') == 'assign_task':  # اگر عملیات اختصاص تسک باشد
#             task_id = data.get('task_id')
#             await self.assign_task(task_id)
#
#     # تخصیص تسک به پیک
#     async def assign_task(self, task_id):
#         task = await self.get_task(task_id)
#         if task:
#             # تغییر گروه کانال به گروه تسک مربوطه
#             await self.channel_layer.group_discard(self.vehicle_group, self.channel_name)
#             await self.channel_layer.group_add(f"task_{task.id}", self.channel_name)
#             await self.channel_layer.group_send(
#                 f"task_{task.id}",
#                 {'type': 'task_assigned', 'message': f'Task {task.id} assigned to courier {self.user.username}'}
#             )
# class CourierConsumer(BaseConsumer):
#     async def connect(self):
#         # دریافت کاربر احراز هویت شده
#         self.user = await self.get_authenticated_user()
#
#         # اگر کاربر احراز هویت نشده باشد یا پیک نباشد، اتصال قطع می‌شود
#         if not self.user or not await self.is_courier():
#             await self.close()
#         else:
#             vehicle_type = await self.get_vehicle_type()  # دریافت نوع وسیله نقلیه
#             self.vehicle_group = f"vehicle_{vehicle_type}"  # نام گروه بر اساس نوع وسیله نقلیه
#             await self.channel_layer.group_add(self.vehicle_group, self.channel_name)
#             await self.accept()
#
#     # بررسی اینکه آیا کاربر یک پیک است
#     @database_sync_to_async
#     def is_courier(self):
#         return Courier.objects.filter(user=self.user).exists()
#
#     # دریافت نوع وسیله نقلیه پیک
#     @database_sync_to_async
#     def get_vehicle_type(self):
#         courier = Courier.objects.get(user=self.user)
#         print(courier.vehicle_type)
#         return courier.vehicle_type
#
#     # قطع اتصال از کانال
#     async def disconnect(self, close_code):
#         if hasattr(self, 'vehicle_group'):
#             await self.channel_layer.group_discard(self.vehicle_group, self.channel_name)
#
#     # دریافت داده‌ها از کلاینت
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         if data.get('action') == 'assign_task':  # اگر عملیات اختصاص تسک باشد
#             task_id = data.get('task_id')
#             await self.assign_task(task_id)
#
#     # تخصیص تسک به پیک
#     async def assign_task(self, task_id):
#         task = await self.get_task(task_id)
#         if task:
#             # تغییر گروه کانال به گروه تسک مربوطه
#             await self.channel_layer.group_discard(self.vehicle_group, self.channel_name)
#             await self.channel_layer.group_add(f"task_{task.id}", self.channel_name)
#             await self.channel_layer.group_send(
#                 f"task_{task.id}",
#                 {'type': 'task_assigned', 'message': f'Task {task.id} assigned to courier {self.user.username}'}
#             )
#
#     # دریافت تسک بر اساس شناسه
#     @database_sync_to_async
#     def get_task(self, task_id):
#         return Task.objects.filter(id=task_id, status='pending').first()
#
#     # ارسال پیام تخصیص تسک به پیک
#     async def task_assigned(self, event):
#         await self.send(text_data=json.dumps({'message': event['message']}))
#
#
#
