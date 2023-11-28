import logging
from functools import partial, update_wrapper
from typing import Tuple, TypeVar, Mapping, Dict

from channels.consumer import get_handler_name, AsyncConsumer
from channels.exceptions import InvalidChannelLayerError, DenyConnection, AcceptConnection
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.utils import await_many_dispatch
from channels_redis.core import RedisChannelLayer


logger = logging.getLogger(__name__)


RCL = TypeVar('RCL', bound=RedisChannelLayer)
MsgVar = Mapping


class SocketMessage:
    __slots__ = ()


class TerminalCommand(SocketMessage):
    __slots__ = ()


class TerminalOutput(SocketMessage):
    __slots__ = ()




class TerminalConsumer:

    __slots__ = ('scope', 'redis_layer', 'ch_name', 'ch_recv_func',
                 'ch_send_func', 'groups',)

    async def __call__(self, scope, receive, send):
        """
        Dispatcher
        """
        self.scope = scope

        self.redis_layer: RCL = get_channel_layer('terminal')

        self.ch_name = await self.redis_layer.new_channel()

        self.ch_send_func = send

        self.ch_recv_func = partial(self.redis_layer.receive, self.ch_name
                                    )
        await await_many_dispatch([receive, self.ch_recv_func], self.dispatch)

    async def dispatch(self, message):
        handler = getattr(self, get_handler_name(message), None)
        if handler:
            await handler(message)
        else:
            raise ValueError("No handler for message type %s" % message["type"])

    async def send(self, message):
        await self.ch_send_func(message)

    async def on_connection_made(self):
        logger.debug('client wants to connect...')
        try:
            for group in self.groups:
                await self.redis_layer.group_add(group, self.ch_name)
        except AttributeError:
            raise InvalidChannelLayerError(
                "BACKEND is unconfigured or doesn't support groups"
            )
        try:
            await self.connect()
        except AcceptConnection:
            await self.accept()
        except DenyConnection:
            await self.close()

    async def accept_connection(self, subprotocol=None):
        logger.debug('accepting socket connection')
        await self.send({"type": "websocket.accept", "subprotocol": subprotocol})

    async def on_data_received(self):
        pass

    @classmethod
    def as_asgi(cls, **initkwargs):
        """
        Return an ASGI v3 single callable that instantiates a consumer instance
        per scope. Similar in purpose to Django's as_view().

        initkwargs will be used to instantiate the consumer instance.
        """

        async def app(scope, receive, send):
            consumer = cls(**initkwargs)
            return await consumer(scope, receive, send)

        app.consumer_class = cls
        app.consumer_initkwargs = initkwargs

        # take name and docstring from class
        update_wrapper(app, cls, updated=())
        return app

