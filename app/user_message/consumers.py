import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Message, Thread


class MessageConsumer(AsyncConsumer):
    async def websocket_connect(self, event):

        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']

        thread_obj = await self.get_thread(me, other_user)
        chat_room = f"thread_{thread_obj.id}"

        self.chat_room = chat_room
        self.thread_obj = thread_obj

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            'type': "websocket.accept"
        })

    async def websocket_receive(self, event):
        """
        When message us received from the websocketss
        """

        msg = event.get('text', None)

        user = self.scope['user']
        username = 'default'

        if user.is_authenticated:
            username = user.username

        my_response = {
            'message': msg,
            'username': username
        }

        await self.create_new_chat_message(user, msg)

        # Broadcasts message to the group
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                "text": json.dumps(my_response)
            }
        )

    # sends actual message
    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        """
        when socket disconnects
        """

        await self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name
        )

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_new_chat_message(self, me, msg):
        thread_obj = self.thread_obj
        return Message.objects.create(thread=thread_obj, user=me, message=msg)
