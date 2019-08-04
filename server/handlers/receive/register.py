from handler import Handler


class Register(Handler):
    @property
    def code(self):
        return 0x02

    def execute(self, socket, room):
        print('User at {} is trying to register'.format(socket.remote_address))