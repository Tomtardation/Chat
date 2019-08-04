from handlers.handler import Handler
from handlers.receive import login


class LoginAcknowledgement(Handler):
    def __init__(self, log):
        self.log = log

    @property
    def code(self):
        return 0x04

    async def execute(self, packet, socket, id):
        packet.writeInteger(id)
        self.log.info('User ({}) at {} acknowledged login.'.format(id, socket.remote_address))