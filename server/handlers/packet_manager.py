#from config.configuration_loader import ConfigurationLoader
from handlers.handler import Handler
from handlers.receive.login import Login

class PacketManager():
    def __init__(self, log):
        self.__handlers__ = {}
        #self.configuration = ConfigurationLoader()
        self.log = log
        #self.log = self.configuration.getLogger()
        self.add(Login(self.log))
        print(1 in self.__handlers__)
    

    def add(self, handler):
        if (issubclass(type(handler), Handler)):
            self.__handlers__[handler.code] = handler
        else:
            raise Exception("Cannot add non-handler to handler service.")
    

    async def handle(self, packet, socket):
        code = packet.readShort()

        if code in self.__handlers__:
            await self.__handlers__[code].execute(packet, socket)
        else:
            self.log.error("Found unhandled packet code ({}): {}".format(code, ''.join('{:02x}'.format(x) for x in packet.toByteArray())))