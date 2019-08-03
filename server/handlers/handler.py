from abc import ABC, abstractmethod, abstractproperty

class Handler(ABC):
    def __init__(self):
        super().__init__()

    @abstractproperty
    def code(self):
        pass

    @abstractmethod
    async def execute(self, socket, room):
        pass