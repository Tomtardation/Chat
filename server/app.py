import sys
sys.path.append("")

import asyncio
from utils.byte_stream import ByteStream
from concurrent.futures import TimeoutError
import os
from utils.configuration_loader import ConfigurationLoader
import ssl
import time
import traceback
import websockets
from handlers.packet_manager import PacketManager
import pathlib


# Variables
cl = ConfigurationLoader()
log = cl.getLogger()
handlers = PacketManager(cl, log)
loop = asyncio.get_event_loop()


# Functions
async def connection(socket, path):
    log.info("Opening connection from {} on {}.".format(socket.remote_address, path))

    while True:
        try:
            message = await socket.recv()
            log.debug("< Packet from {}: {}".format(socket.remote_address, ''.join('{:02x}'.format(x) for x in message)))
            buffer = ByteStream(message)
            await handlers.handle(buffer, socket)
        except websockets.exceptions.ConnectionClosedOK:
            log.info("Closing connection from {} on {}".format(socket.remote_address, path))
            break
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            break


# Main
if __name__ == '__main__':
    log.info("Fetching SSL certificates.")
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    localhost_cert = os.path.relpath(cl.get('ssl_cert'))
    localhost_key = os.path.relpath(cl.get('ssl_key'))
    #print(localhost_pem, localhost_key, ssl_context)
    ssl_context.load_cert_chain(localhost_cert, keyfile=localhost_key)

    log.info("Starting websocket.")
    server = websockets.serve(connection, "localhost", 8766, ssl=ssl_context)

    log.info("Starting main event loop.")
    try:
        loop.run_until_complete(server)
        asyncio.get_event_loop().run_forever()
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        log.error(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    finally:
        log.warning("Main event loop closing.")
        loop.close()