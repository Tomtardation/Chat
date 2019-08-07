let rpacket_manager = new ReceivePacketManager();
let spacket_manager = new SendPacketManager();

let socket = new WebSocket('wss://localhost:8443/server');
socket.binaryType = 'arraybuffer';

socket.onopen = async () => {
    console.log('Socket connected');

    //let login = new LoginHandler().createPacket(socket, "Poop");
    //await socket.send(new Uint8Array(login).buffer);
}

socket.onmessage = async (e) => {
    console.log("Message received: " + e.data);

    let reader = new BinaryReader(e.data);
    let code = reader.readShort();

    let handler = rpacket_manager.get(code);
    if (handler != null) {
        handler.execute(reader, socket, {})
    } else {
        console.error("Found unhandled packet from server: " + code);
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

    button.addEventListener("click", (e) => {
        let username_input = document.getElementById("username");
        let password_input = document.getElementById("password");
        let username = username_input.value;
        let password = password_input.value;
        
        let packet = new LoginHandler().createPacket(socket, username, password);
        return socket.send(new Uint8Array(packet).buffer);
    });
});