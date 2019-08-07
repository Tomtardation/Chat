class ReceiveHandler {
    constructor(code) {
        this.code = code
    }

    execute(packet, server, user) {
        throw new Error("Not implemented.");
    }
}

class LoginAcknowledgementHandler extends ReceiveHandler {
    constructor() {
        super(0x04);
    }

    execute(packet, server, user) {
        let error_code = packet.readShort();

        if (error_code == 0) {
            let userid = packet.readInteger();
            user['id'] = userid;
            console.log("User ID:", userid);
        } else {
            // TODO: show error message and code.
            console.log("Failed attempt.");
        }
    }
}

// Packets from server

class ReceivePacketManager {
    constructor() {
        this.handlers = {}

        this.add(new LoginAcknowledgementHandler());
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

    createPacket(server, username, password) {
        let buffer = new BinaryWriter();
        super.setup(buffer);
        buffer.writeString(username);
        buffer.writeString(password);
        return buffer.toArray();
    }
}

class SendMessageHandler extends SendHandler {
    constructor() {
        super(0x01);
    }

    createPacket(server, id, message) {
        let buffer = new BinaryWriter();
        super.setup(buffer);
        buffer.writeString(username);
        return buffer;
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