from handler import Handler


class Login(Handler):
    @property
    def code(self):
        return 0x01

    def execute(self, socket, room):
        print('hello')