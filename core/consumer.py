import asyncio
import os
import pty
import shutil
import struct
import sys

import termios

import fcntl
import json
from asyncio import (
    get_event_loop,
    ensure_future,
    sleep
)
from asyncio.subprocess import (
    SubprocessStreamProtocol, Process, PIPE, STDOUT,  # noqa

)
import logging
from shlex import quote, split
from typing import TypeVar, Mapping, Dict, Tuple, Union

from channels.generic.websocket import AsyncWebsocketConsumer
from channels_redis.core import RedisChannelLayer
from rich.pretty import pprint

logger = logging.getLogger(__name__)

RCL = TypeVar('RCL', bound=RedisChannelLayer)
MsgVar = Mapping


LIMIT = 2**8


def set_winsize(fd, col, row):
    s = struct.pack("HHHH", row, col, 0, 0)
    termios.tcsetattr(fd, termios.TIOCGWINSZ, [row, col])


async def create_shell_process() -> Process:
    pprint(sys.stdout.isatty())


    loop = get_event_loop()
    tran, prot = await loop.subprocess_shell(
        lambda: SubprocessStreamProtocol(limit=LIMIT, loop=loop),
        '/bin/bash',
        stderr=PIPE, stdout=PIPE, stdin=PIPE, env={'TERM': 'xterm-256color'},
    )
    return Process(tran, prot, loop=loop)


class TerminalConsumer(AsyncWebsocketConsumer):
    """ASGI compatible Terminal Consumer without channel layer.
       Provides an asynchronous shell process to communicate with over
       Streamreader and Streamwriter classes.
       Only grants superuser access. (User object is added in AuthMiddleware)
    """
    __slots__ = ('proc', '_sizes', '_fd_stdin')

    def __init__(self):
        super().__init__()
        self.proc: Process | None = None
        self._sizes = {"cols": 180, "rows": 15}
        self._fd_stdin: int | None = None

    async def connect(self):
        user = self.scope.get('user')
        if user and user.is_superuser:
            await self.accept()

            self.proc = await create_shell_process()
            await self.get_pty()
            pprint(self.proc)
            ensure_future(self.run_interactive())
        else:
            await self.close(code=4000)

    async def disconnect(self, close_code):
        try:
            if self.proc:
                self.proc.terminate()
                await self.proc.wait()
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")
        finally:
            await super().disconnect(close_code)

    async def websocket_receive(self, data):
        """Dispatches keypresses and resize requests"""
        pprint(data)
        text = data['text']
        if len(text) == 1:
            await self.receive_key(text)
        elif '["resize",{"cols"' in text:
            await self.on_resize(json.loads(text)[1])

    async def receive_key(self, key) -> None:
        k = key.replace('\r', '\n') if key == '\r' else key
        await self.send_to_process(k)

    async def send_to_process(self, data: Union[bytes, str]) -> None:
        """Wrapper for write and drain"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.proc.stdin.write(data)
        await self.proc.stdin.drain()

    async def on_resize(self, sizes: Dict[str, int]):
        """Resizes pty dimensions to fit to terminal element"""
        if sizes != self._sizes:
            self._sizes = sizes
            pprint(self._sizes)

    async def get_pty(self):
        await sleep(.1)
        await self.send_to_process(
            f'script -qc /bin/bash /dev/null 2>&1;python -c "import termios; termios.tcsetwinsize(1,(15,189));"\n'
            .encode()
        )

    async def run_interactive(self):
        try:
            while True:
                data = await self.proc.stdout.read(100)
                if not data:
                    break
                await self.send(text_data=data.decode('utf-8'))

        except asyncio.CancelledError:
            pass
        finally:
            self.proc.terminate()
            await self.proc.wait()
