from handlers.handler import Handler
from handlers.receive import login


class Login(Handler):
    def __init__(self, log):
        self.log = log
        self.log.info("Testtt")

    @property
    def code(self):
        return 0x01

    async def execute(self, packet, socket):
        self.log.info("Testtt")
        username = packet.readString()
        self.log.info('User ({}) at {} logged in.'.format(username, socket.remote_address))