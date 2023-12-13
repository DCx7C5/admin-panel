import json
import logging
from functools import partial, update_wrapper
from pprint import pprint
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


class TerminalWorker(AsyncWebsocketConsumer):
    __slots__ = ('user',)
    groups = ["terminal"]

    async def connect(self):
        # Called on connection.
        # To accept the connection call:
        user = self.scope['user']
        pprint(self.user)
        for key, val in self.scope.items():
            print(key, val)

        await self.accept()

        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']


    async def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        await self.send(text_data="Hello world!")
        # Or, to send a binary frame:
        await self.send(bytes_data="Hello world!")
        # Want to force-close the connection? Call:
        await self.close()
        # Or add a custom WebSocket error code!
        await self.close(code=4123)

    async def disconnect(self, close_code):
        # Called when the socket closes
        logger.info('Disconnected from')
