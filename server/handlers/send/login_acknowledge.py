from handlers.handler import Handler
from handlers.receive import login


class LoginAcknowledgement(Handler):
    def __init__(self, log):
        self.log = log

    @property
    def code(self):
        return 0x04

    async def execute(self, packet, socket, error_code, id):
        packet.writeShort(error_code)
        if error_code == 0 and id is not None:
            packet.writeInteger(id)
            self.log.info('User ({}) at {} acknowledged login.'.format(id, socket.remote_address))

            # TODO: send room data to user.
        else:
            self.log.warn('User at {} attempted login.'.format(socket.remote_address))