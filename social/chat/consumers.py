import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

from social.chat.models import Chat, Room


User = get_user_model()


class ChatRoomConsumer(AsyncWebsocketConsumer):
    """connect"""
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.room = await self.get_room()
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    """Disconnect"""
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer
        )

    """Receive"""
    async def receive(self, text_data):
        if text_data:
            text_data_json = json.loads(text_data)

            text = text_data_json['text']

            await self.create_message(text)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chatroom_message',
                    'message': json.dumps({'sender': self.user.username, 'text': text}),
                    'sender_channel_name': self.channel_name
                }
            )

    """Message"""
    async def chatroom_message(self, event):
        message = event['message']

        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=message)

    @database_sync_to_async
    def get_room(self):
        try:
            room = Room.objects.get(room_id=self.room_id)
            return room
        except Room.DoesNotExist:
            return None


    @database_sync_to_async
    def create_message(self, text):
        Chat.objects.create(room_id=self.room, author=self.user, text=text)
