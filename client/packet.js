class ReceiveHandler {
    constructor(code) {
        this.code = code
    }

    execute(packet, server) {
        throw new Error("Not implemented.");
    }
}

// Packets from server

class ReceivePacketManager {
    constructor() {
        this.handlers = {}
    }

    add(handler) {
        this.handlers[handler.code] = handler;
    }

    get(code) {
        return this.handlers[code];
    }
}


// Packets to server
class SendHandler {
    constructor(code) {
        this.code = code
    }

    createPacket(server) {
        throw new Error("Not implemented.");
    }

    setup(buffer) {
        buffer.writeShort(this.code);
    }
}

class LoginHandler extends SendHandler {
    constructor() {
        super(0x01);
    }

    createPacket(server, username) {
        let buffer = new BinaryWriter();
        super.setup(buffer);
        buffer.writeString(username);
        return buffer.toArray();
    }
}

class SendPacketManager {
    constructor() {
        this.handlers = {}
    }

    add(handler) {
        this.handlers[handler.code] = handler;
    }

    get(code) {
        return this.handlers[code];
    }
}