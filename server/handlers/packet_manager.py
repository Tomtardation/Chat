from utils.byte_stream import ByteStream
from handlers.handler import Handler
from handlers.receive.login import Login
from handlers.receive.version_check import VersionCheck
from handlers.send.login_acknowledge import LoginAcknowledgement
from handlers.send.version_acknowledge import VersionAcknowledgement
import logging

class PacketManager():
    def __init__(self, config, log):
        self.__recvhandlers__ = {}
        self.__sendhandlers__ = {}
        self.cl = config
        self.log = log

        self.__add__(VersionCheck(self.cl, self.log), self.__recvhandlers__)
        self.__add__(Login(self.log), self.__recvhandlers__)

        self.__add__(VersionAcknowledgement(self.log), self.__sendhandlers__)
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

    async def handle(self, websocket, request, message):
        code = message.buffer.readShort()

        if code in self.__recvhandlers__:
            await self.__recvhandlers__[code].execute(self, websocket, request, message.buffer)
        else:
            logging.error("Found unhandled packet code ({}): {}".format(code, ''.join('{:02x}'.format(x) for x in message.buffer.toByteArray())))

    async def send(self, code, websocket, *args):
        packet_struct = self.getSendPacket(code)
        if packet_struct is not None:
            data = ByteStream()
            data.writeShort(code)
            await packet_struct.execute(data, *args)
            await websocket.send_bytes(data.toByteArray())