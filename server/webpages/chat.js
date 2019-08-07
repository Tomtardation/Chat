let rpacket_manager = new ReceivePacketManager();
let spacket_manager = new SendPacketManager();
let user = {};

let socket = new WebSocket('ws://localhost:8766');
socket.binaryType = 'arraybuffer';

socket.onopen = async () => {
    console.log('Socket connected');

    // let login = new LoginHandler().createPacket(socket, "Poop");
    // await socket.send(new Uint8Array(login).buffer);
}

socket.onmessage = async (e) => {
    console.log("Message received: " + e.data);

    let reader = new BinaryReader(e.data);
    let code = reader.readShort();

    let handler = rpacket_manager.get(code);
    if (handler != null) {
        handler.execute(reader, socket, user);
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

document.addEventListener("DOMContentLoaded", () => {
    let button = document.getElementById("submit");

    button.addEventListener("keypress", (e) => {
        if (e.keyCode != 13 || e.shiftKey)
            return;
        
        let input = document.getElementById("text");
        let message = input.value;

        if (message == null || message.length == 0)
            return;
        
        let packet = new SendMessageHandler().createPacket(socket, user.id, message);
        return socket.send(new Uint8Array(packet.toArray()).buffer);
    });
});