from OpenSSL.rand import status
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


class Group_Selecter_Consumer(BaseConsumer):
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
            # task = await database_sync_to_async(Task.objects.filter(status="pending").order_by('-id').first)()
            task = await database_sync_to_async(Task.objects.order_by('-id').first)()
            print(task)
            if not task:
                print("No pending tasks found.")
                await self.close()
                return
            elif task.status =="pending":
                vehicle_type = task.vehicle_type
                self.room_group_name = f"public_group_{vehicle_type}"
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.accept()
            elif task.status in [ "accepted","in_transit"]:
                vehicle_type = task.vehicle_type
                self.room_group_name = f"private_group_{task.id}_{vehicle_type}"
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.accept()
            elif task.status in [ "delivered","canceled"]:
                await self.close()
                return
        except Exception as e:
            print(f"An error occurred: {e}")
            await self.close()

    async def handle_courier(self):
        """مدیریت ورود پیک و تخصیص گروه عمومی بر اساس وسیله نقلیه"""
        print("User is a courier ...")
        try:
            courier = await database_sync_to_async(Courier.objects.get)(user=self.user)
            print(courier)
            if courier.status == "online":
                vehicle_type = courier.vehicle_type
                self.room_group_name = f"public_group_{vehicle_type}"
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.accept()
            elif courier.status in [ "at_work",]:
                task = await database_sync_to_async(Task.objects.filter(courier=courier).order_by('-id').first)()
                print(f"private_group_{task.id}")
                self.room_group_name = f"private_group_{task.id}"
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.accept()
            elif courier.status in ["offline", ] :
                print("offline user cant go into a public group")
                task_count = await database_sync_to_async(Task.objects.filter(courier=courier , status="accepted").order_by('-id')).count()
                task = await database_sync_to_async(Task.objects.filter(courier=courier , status="accepted").order_by('-id')).first()
                if task_count >0 :
                    print(f"private_group_{task.id}")
                    self.room_group_name = f"private_group_{task.id}"
                    await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                    await self.accept()

                elif courier.status not in ["online", "at_work", "offline"]:
                    print(f"Invalid courier status: {courier.status}")
                    await self.close()
                    return
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

    async def sender_chat_message(self, event):
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
    async def courier_chat_message(self, event):
        await self.send(text_data=json.dumps({
            'action': event['action'],
            'message': event['message'],
            'courier_id': event['courier_id'],
            'status': event['status'],
        }))
        print(f"Message received in consumer: {event['message']}")
