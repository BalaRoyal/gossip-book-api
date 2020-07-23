import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async


class NotificationConsumer(AsyncConsumer):
    async def websocket_connect(self, event):

        user = self.scope['user']
        self.room_name = f'notification_{user.id}'

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name)

        await self.send({
            'type': 'websocket.accept'
        })

    async def notification_message(self, event):
        """ Send user notifications. """

        await self.send({
            'type': 'websocket.send',
            'text': event['data']
        })

    async def websocket_disconnect(self, event):
        """Discard channel group when socket is disconnected."""

        await self.channel_layer.group_discard(self.room_name,
                                               self.channel_name)
