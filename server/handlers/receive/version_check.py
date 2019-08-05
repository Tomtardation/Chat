import base64
import binascii
from handlers.handler import Handler
from handlers.receive import login
import os
import hashlib
import random


class VersionCheck(Handler):
    def __init__(self, cl, log):
        self.cl = cl
        self.log = log

    @property
    def code(self):
        return 0x01

    async def execute(self, manager, packet, socket):
        recv_major = packet.read()
        recv_minor = packet.read()
        recv_build = packet.readInteger()

        major = self.cl.get('major')
        minor = self.cl.get('minor')
        build = self.cl.get('build')

        value = 1 if recv_major == major and recv_minor == minor and recv_build == build else 0
        await manager.send(0x01, socket, value)

