import json
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.layers import get_channel_layer

from chat.models import Chat_Application, MessageUser

all_users_use_page_my_chat = 'my_chats'
channel_layer = get_channel_layer()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.chat = self.get_name_chat()

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        chat = await self.get_name_chat()
        cur_user, photo, now_time = await self.get_data_user()
        print(cur_user, photo, now_time)

        print(message)
        print(self.user)

        await self.save_message_in_bd(message=message, user=self.user, chat=chat)


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message, "cur_user": cur_user, "photo": photo, "now_time": now_time}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        cur_user, photo, now_time = await self.get_data_user()
        #print(message)
        # Send message to WebSocket
#        await channel_layer.group_send(
#            all_users_use_page_my_chat,
#            {"type": "on.message", "message": message, "cur_user": cur_user, "photo": photo, "now_time": now_time},
#        )

        await self.send(text_data=json.dumps({"message": message, "cur_user": cur_user, "photo": photo, "now_time": now_time}))

    @database_sync_to_async
    def get_name_chat(self):
       if self.room_name == 'general-chat':
           room_name = 'General Chat'
       else:
           room_name = self.room_name

       return Chat_Application.objects.get(name_chat=room_name)

    @database_sync_to_async
    def save_message_in_bd(self, message, user, chat):
        print(message, user, chat)
        MessageUser.objects.create(text=message, users_send=user, chat_it_is=chat)

    @database_sync_to_async
    def get_data_user(self):
        return self.user.username, self.user.profile_picture.url, str(datetime.now())


class View_last_message_in_chats(AsyncWebsocketConsumer):
    # Receive message from room group
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = all_users_use_page_my_chat

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        print(text_data_json)
        print(text_data_json['message'])

        #await self.save_message_in_bd(message=message, user=self.user, chat=chat)

        # Send message to room group
        #await self.channel_layer.group_send(
        #    self.room_group_name,
        #   {"type": "chat.message", "message": message, "cur_user": cur_user, "photo": photo, "now_time": now_time}
        #)


    async def chat_message(self, event):
        message = event["message"]
        cur_user, photo, now_time = await self.get_data_user()
        #print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "cur_user": cur_user, "photo": photo, "now_time": now_time}))


