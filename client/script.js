let rpacket_manager = new ReceivePacketManager();
let spacket_manager = new SendPacketManager();

let socket = new WebSocket('ws://localhost:8766');
socket.binaryType = 'arraybuffer';

socket.onopen = async () => {
    console.log('Socket connected');

    /*let writer = new BinaryWriter();
    writer.writeShort(0x01);
    writer.writeString("Hello World 1");*/
    let login = new LoginHandler().createPacket(socket, "Poop");
    await socket.send(new Uint8Array(login).buffer);
}

socket.onmessage = async (e) => {
    console.log("Message received: " + e.data);

    let reader = new BinaryReader(e.data);
    let code = reader.readShort();

    let handler = rpacket_manager.get(code);
    if (handler != null) {
        handler.execute(reader, socket)
    } else {
        console.error("Found unhandlded packet from server: " + code);
    }
}

socket.onclose = (e) => {
    console.log("Connection closed:", e);
}

socket.onerror = (e) => {
    console.log("Connection error:", e);
}