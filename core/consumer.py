import json
import logging
from functools import partial, update_wrapper
from typing import Tuple, TypeVar, Mapping, Dict, Any, Coroutine

from channels.consumer import get_handler_name, AsyncConsumer
from channels.exceptions import InvalidChannelLayerError, DenyConnection, AcceptConnection
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.utils import await_many_dispatch
from channels_redis.core import RedisChannelLayer

logger = logging.getLogger(__name__)

RCL = TypeVar('RCL', bound=RedisChannelLayer)
MsgVar = Mapping


class CoreConsumer(AsyncWebsocketConsumer): ...


class TerminalWorker(AsyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.room_group_name = None
        self.room_name = None

    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

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

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
