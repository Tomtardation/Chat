import base64
import binascii
from handlers.handler import Handler
from handlers.receive import login
import os
import hashlib


class Register(Handler):
    def __init__(self, log):
        self.log = log

    @property
    def code(self):
        return 0x01

    async def execute(self, manager, packet, socket):
        username = packet.readString()
        password = packet.readString()
        self.log.info('User ({}) at {} logged in.'.format(username, socket.remote_address))
        print(password)

        salt = base64.b64encode(hashlib.sha256(os.urandom(64)).digest())
        hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 2048)
        print('HASH', str(hash))
        print('HASH DECODED', base64.b64encode(hash).decode('utf-8'))
        print('salt', salt.decode('utf-8'))

        await manager.send(self.code, socket, id)


        log.info('User at {} is trying to register'.format(socket.remote_address))