import ipaddress

class ClientManager():
    def __init__(self):
        self.clients = {}
    
    def add(self, name, socket):
        ip_value = int(ipaddress.IPv4Address(socket.remote_address))
        self.clients[ip_value] = Client(name, socket)
