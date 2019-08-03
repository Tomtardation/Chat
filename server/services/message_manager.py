class MessageManager():
    def __init__(self):
        self.__handlers__ = {}
    

    def add(self, handler):
        if (issubclass(handler, Handler)):
            self.__handlers__[type(handler).__name__.lower()] = handler
        else:
            raise Exception("Cannot add non-handler to handler service.")