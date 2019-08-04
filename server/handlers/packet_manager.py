from utils.byte_stream import ByteStream
#from config.configuration_loader import ConfigurationLoader
from handlers.handler import Handler
from handlers.receive.login import Login
from handlers.send.login_acknowledge import LoginAcknowledgement

class PacketManager():
    def __init__(self, log):
        self.__recvhandlers__ = {}
        self.__sendhandlers__ = {}
        #self.configuration = ConfigurationLoader()
        self.log = log
        #self.log = self.configuration.getLogger()

        self.__add__(Login(self.log), self.__recvhandlers__)

        self.__add__(LoginAcknowledgement(self.log), self.__sendhandlers__)
    

    def __add__(self, handler, handlers):
        if (issubclass(type(handler), Handler)):
            handlers[handler.code] = handler
        else:
            raise Exception("Cannot add non-handler to handler service.")
    

    def getRecvPacket(self, code):
        if code in self.__recvhandlers__:
            return self.__recvhandlers__[code]
        return None

    def getSendPacket(self, code):
        if code in self.__sendhandlers__:
            return self.__sendhandlers__[code]
        return None


    async def handle(self, packet, socket):
        code = packet.readShort()

        if code in self.__recvhandlers__:
            await self.__recvhandlers__[code].execute(self, packet, socket)
        else:
            self.log.error("Found unhandled packet code ({}): {}".format(code, ''.join('{:02x}'.format(x) for x in packet.toByteArray())))
    

    async def send(self, code, socket, *args):
        packet_struct = self.getSendPacket(code)
        if packet_struct is not None:
            data = ByteStream()
            data.writeShort(code)
            await packet_struct.execute(data, socket, *args)
            await socket.send(data.toByteArray())