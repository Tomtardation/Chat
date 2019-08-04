from handlers.handler import Handler
from handlers.receive import login
import random


class Login(Handler):
    def __init__(self, log):
        self.log = log

    @property
    def code(self):
        return 0x01

    async def execute(self, manager, packet, socket):
        username = packet.readString()
        self.log.info('User ({}) at {} logged in.'.format(username, socket.remote_address))

        id = random.randint(0, 100)
        await manager.send(0x04, socket, id)

