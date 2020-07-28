import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async


class QuestionConsumer(AsyncConsumer):
    async def websocket_connect(self, event):

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        """"[summary]"

        Args:
            event ([type]): [description]
        """

        print('receive', event)

        await self.send({
            'type': 'websocket.receive'
        })

    async def websocket_disconnect(self, event):
        """[summary]

        Args:
            event ([type]): [description]
        """

        print('disconnected', event)
