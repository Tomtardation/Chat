import base64
import binascii
from handlers.handler import Handler
from handlers.receive import login
import os
import hashlib
import random


class Login(Handler):
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

        # TODO: fetch salt & hash from database
        # TODO: compare hash together.
        salt = base64.b64encode(hashlib.sha256(os.urandom(64)).digest())
        hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 2048)
        print('HASH', str(hash))
        print('HASH DECODED', base64.b64encode(hash).decode('utf-8'))
        print('salt', salt.decode('utf-8'))

        error_code = 0 if random.randint(0, 100) < 50 else 1

        id = random.randint(0, 100)
        await manager.send(0x04, socket, error_code, id if error_code == 0 else None)