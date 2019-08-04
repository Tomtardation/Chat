from io import BytesIO as Bytes, StringIO as String

class ByteStream():
    def __init__(self, byte_array = None):
        self.buffer = Bytes(byte_array) or Bytes()
        self.size = self.buffer.getbuffer().nbytes
        self.position = 0

    
    def flip(self):
        self.position = 0

    def read(self, signed = True):
        return self.__readNumber__(1, signed=signed)

    def readInteger(self, signed = True):
        return self.__readNumber__(4, signed=signed)
    
    def readLong(self, signed = True):
        return self.__readNumber__(8, signed=signed)

    def readShort(self, signed = True):
        return self.__readNumber__(2, signed=signed)
    
    def readString(self):
        length = self.readShort(signed = False)
        return self.__readValue__(length).decode("utf-8")

    def __readValue__(self, size):
        if self.position + size > self.size:
            raise Exception("ArrayOutOfBounds")

        value = self.buffer.read(size)
        self.position += size
        return value
    
    def __readNumber__(self, size, signed = True):
        value = self.__readValue__(size)
        return int.from_bytes(value, byteorder='big', signed=signed)

    def toByteArray(self):
        return self.buffer.getbuffer()

    def write(self, byte):
        self.__writeArray__(byte)

    def writeInteger(self, integer, signed = True):
        self.__writeNumber__(integer, 4, signed = signed)

    def writeLong(self, long, signed = True):
        self.__writeNumber__(long, 8, signed = signed)

    def writeShort(self, short, signed = True):
        self.__writeNumber__(short, 2, signed = signed)
    
    def writeString(self, string):
        self.writeShort(len(string), signed = False)
        byte_array = Bytes(string.encode("utf-8"))
        for x in byte_array:
            self.write(x)

    def __writeArray__(self, array):
        buffer = Bytes(array)
        self.buffer.write(buffer.getbuffer())
        self.size += buffer.getbuffer().nbytes

    def __writeNumber__(self, value, size, signed = True):
        array = value.to_bytes(size, byteorder='big', signed=signed)
        self.__writeArray__(array)
    
