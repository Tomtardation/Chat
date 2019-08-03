import asyncio
from concurrent.futures import TimeoutError
from io import BytesIO as Bytes
from byte_stream import ByteStream
import time
import websockets
from services.message_manager import MessageManager


def on_receive(message, test = False):
    print(f"< RAW: " + ''.join('{:02x}'.format(x) for x in message))
    buffer = ByteStream(message)
    message = buffer.readString()
    print("< DECODED (message):", message)

    if test:
        message2 = buffer.readString()
        print("< DECODED (message2):", message2)
        number = buffer.readShort()
        print("< DECODED (number):", number)


async def connection(socket, path):
    print("Opening connection from", socket.remote_address, path)

    message = await socket.recv()
    on_receive(message)

    buffer = ByteStream()
    buffer.writeString('Hello')
    await socket.send(buffer.toByteArray())
    print(f"> Message sent")

    try:
        message = await asyncio.wait_for(socket.recv(), 3)
        on_receive(message, test = True)
        await asyncio.sleep(3)
    except TimeoutError as e:
        print("No second message received from", socket.remote_address)
        await socket.close()

    print("Closing connection from", socket.remote_address)


#client_manager = ClientManager()
handlers = MessageManager()

server = websockets.serve(connection, "localhost", 8766)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()