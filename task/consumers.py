import json
from channels.generic.websocket import AsyncWebsocketConsumer


# class TaskConsumer(AsyncWebsocketConsumer):
#
#     async def connect(self):
#         # گرفتن task_id از URL
#         self.task_id = self.scope['url_route']['kwargs'].get('task_id', None)
#         print(self.task_id)
#         print(f"Task ID:::: {self.task_id}")
#         print("###############")
#         # print(self.task.id)
#
#         # اگر task_id وجود دارد، به گروه مربوطه متصل شوید
#         if self.task_id:
#             print(self.task_id)
#             # print("######///#######")
#
#             self.room_group_name = f'task_{self.task_id}'
#             # print(self.room_group_name)
#             # print("######...#######")
#
#
#             # اتصال به گروه
#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name
#             )
#             print(f"Joined room group: {self.room_group_name}")
#         else:
#             print("No task_id provided in the URL!")
#
#         # پذیرفتن اتصال WebSocket
#         await self.accept()
#         print("######.TTT.#######")
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
import urllib.parse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from task.models import Task


class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # استخراج task_id از URL
        self.task_id = self.scope['url_route']['kwargs'].get('task_id')
        print(self.task_id)
        print("#3333*")

        # استخراج توکن از query string
        query_string = self.scope['query_string'].decode()
        print(query_string)
        query_params = urllib.parse.parse_qs(query_string)
        print(query_params)
        token_key = query_params.get('token', [None])[0]
        print(token_key)

        # پیدا کردن کاربر از روی توکن
        self.user = await self.get_user_from_token(token_key)
        print(self.user)
        print("#44444444*")

        if self.user is None or isinstance(self.user, AnonymousUser):
            print("token motabar nist")
            await self.close()
        elif not await self.has_permission():
            print("dastrasi be task nist")
            await self.close()
        else:
            print("etesal bargharar shod")
            # افزودن کاربر به گروه تسک
            self.room_group_name = f"task_{self.task_id}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    @database_sync_to_async
    def get_user_from_token(self, token_key):
        try:
            print("^^^^^^")
            print(token_key)
            validated_token = JWTAuthentication().get_validated_token(token_key)
            user = JWTAuthentication().get_user(validated_token)
            return user
        except (InvalidToken, TokenError):
            return AnonymousUser()

    @database_sync_to_async
    def has_permission(self):
        task = Task.objects.filter(id=self.task_id).first()
        print(task)
        print("hhhhhhhhhhhhh")
        if task and (task.sender == self.user or (task.courier and task.courier.user == self.user)):
            return True
        return False

    async def disconnect(self, close_code):
        # فقط اگر کاربر sender باشد، اجازه قطع اتصال دارد
        if await self.is_sender():
            if hasattr(self, 'room_group_name'):
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )
                print(f"Sender left room group: {self.room_group_name}")
        else:
            print("Only the sender can disconnect.")

    @database_sync_to_async
    def is_sender(self):
        task = Task.objects.filter(id=self.task_id).first()
        if task and task.sender == self.user:
            return True
        return False


    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        print(f"Received message: {message}")

        # ارسال پیام به گروه
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        print(f"Sending message to WebSocket: {message}")

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def send_task_update(self, event):
        task_id = event['task_id']
        status = event['status']
        print("hhhhh")

        # ارسال پیام به کلاینت WebSocket
        await self.send(text_data=json.dumps({
            'task_id': task_id,
            'status': status,
        }))