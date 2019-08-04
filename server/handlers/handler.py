from abc import ABC, abstractmethod, abstractproperty


class Handler(ABC):
    @abstractproperty
    def code(self):
        pass

    @abstractmethod
    async def execute(self, packet, socket):
        pass