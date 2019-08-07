from handlers.handler import Handler
from handlers.receive import login


class LoginAcknowledgement(Handler):
    def __init__(self, log):
        self.log = log

    @property
    def code(self):
        return 0x04

    async def execute(self, packet, error_code, id):
        packet.writeShort(error_code)
        if error_code == 0 and id is not None:
            packet.writeInteger(id)

            #host, port = request.transport.get_extra_info('peername')
            #self.log.info('User ({}) at {}:{} acknowledged login.'.format(id, host, port))

            # TODO: send room data to user.