class BinaryWriter {
    constructor() {
        this.size = 0;
        this.array = [];
        this.encoder = new TextEncoder();
    }

    write(b) {
        this.array.push(b);
        this.size++;
    }

    writeInteger(integer) {
        this.write((integer >> 24) & 0xFF);
        this.write((integer >> 16) & 0xFF);
        this.write((integer >> 8) & 0xFF);
        this.write((integer >> 0) & 0xFF);
    }

    writeLong(long) {
        this.write((long >> 56) & 0xFF);
        this.write((long >> 48) & 0xFF);
        this.write((long >> 40) & 0xFF);
        this.write((long >> 32) & 0xFF);
        this.write((long >> 24) & 0xFF);
        this.write((long >> 16) & 0xFF);
        this.write((long >> 8) & 0xFF);
        this.write((long >> 0) & 0xFF);
    }

    writeShort(short) {
        this.write((short >> 8) & 0xFF);
        this.write((short >> 0) & 0xFF);
        console.log("SHORT", (short >> 4) & 0xF, (short >> 0) & 0xF)
    }

    writeString(string) {
        let array = this.encoder.encode(string);
        this.writeShort(array.length);

        for (let char of string)
            this.write(char.charCodeAt());
    }

    toArray() {
        return this.array;
    }
}

class BinaryReader2 {
    constructor(array) {
        this.array = array;
        this.view = new DataView(array);
        this.size = array.byteLength;
        this.position = 0;
        this.decoder = new TextDecoder();
    }

    
    readInteger(signed = true) {
        let value = signed ? this.view.getInt32(this.position) : this.view.getUint32(this.position);
        this.position += 4;
        return value;
    }

    readLong(signed = true) {
        let value = (this.readInteger(signed) << 32) | this.readInteger(false);
        return value;
    }

    readShort(signed = true) {
        let value = signed ? this.view.getInt16(this.position) : this.view.getUint16(this.position);
        this.position += 2;
        return value;
    }

    readString() {
        let length = this.readShort();
        let temp = this.array.slice(this.position, this.position + length);
        
        this.position += length;
        return this.decoder.decode(temp);
    }
}

class BinaryReader {
    constructor(array) {
        this.array = array;
        this.size = array.length;
        this.position = 0;
        this.decoder = new TextDecoder();
    }


    read(n = null) {
        if (n == null)
            return this.array[this.position++];
        
        let arr = [];
        let end = this.position + n;
        if (end > this.size)
            throw 'OutOfArrayBounds';

        while (this.position < end)
            arr.push(this.array[this.position++]);
        
        return arr;
    }

    readInteger() {
        return this.readValue(4);
    }

    readLong() {
        return this.readValue(8);
    }

    readShort() {
        return this.readValue(2);
    }

    readString() {
        let length = this.readInteger();
        let array = this.read(length);

        return this.decoder.decode(array);
    }

    readValue(n) {
        let array = this.read(n);
        let value = 0;

        for (let i = 0; i < array.length; i++)
            value += array[i] << (n - i - 1);
        
        return value;
    }
}


let socket = new WebSocket('ws://localhost:8766');
socket.binaryType = 'arraybuffer';


socket.onopen = async () => {
    console.log('Socket connected');

    //let array = encoder.encode("Hello World 1");
    let writer = new BinaryWriter();
    writer.writeString("Hello World 1");
    await socket.send(new Uint8Array(writer.toArray()).buffer);
    return false;
}

socket.onmessage = async (e) => {
    console.log("Message received: " + e.data);

    let reader = new BinaryReader2(e.data);
    let message = reader.readString();
    console.log("Message:", message);
    if (message == "Hello") {
        console.log("Received hello. Sending second message");
        let writer = new BinaryWriter();
        writer.writeString("Hello World 2");
        writer.writeString('Fite me');
        writer.writeShort(1337);
        await socket.send(new Uint8Array(writer.toArray()).buffer);
    }

    return true;
}

socket.onclose = (e) => {
    console.log("Connection closed:", e);
}

socket.onerror = (e) => {
    console.log("Connection error:", e);
}