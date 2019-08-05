from handlers.handler import Handler


class VersionAcknowledgement(Handler):
    def __init__(self, log):
        self.log = log

    @property
    def code(self):
        return 0x01

    # If value = 0, update is required.
    async def execute(self, packet, socket, value):
        packet.write(value)