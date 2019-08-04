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

class BinaryReader {
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