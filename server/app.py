import sys
sys.path.append("")

import aiohttp
from aiohttp import web
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
import logging


# Variables
cl = ConfigurationLoader()
log = cl.getLogger()
handlers = PacketManager(cl, log)
loop = asyncio.get_event_loop()


# Functions
async def connection(websocket, request, message, host, peer):
    try:
        #log.debug("< Packet from {}: {}".format(socket.remote_address, ''.join('{:02x}'.format(x) for x in message.data)))
        # TODO: reject connections from blacklist
        message.buffer = ByteStream(message.data)
        await handlers.handle(websocket, request, message)
    #except websockets.exceptions.ConnectionClosedOK:
    #    log.info("Closing connection from {} on {}".format(socket.remote_address, path))
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        log.error(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))


async def websocket_handler(request):
    try:
        websocket = web.WebSocketResponse()
        if not websocket.can_prepare(request):
            log.debug('Attempted non-websocket connection.')
            return
        
        await websocket.prepare(request)

        peername = request.transport.get_extra_info('peername')
        if peername is None:
            log.info('Rejecting connection without host header.')
            return
        
        host, port = peername
        log.info('Opening connection from {}:{}'.format(host, port))
        
        async for message in websocket:
            print(message.type, message.data, message)
            await connection(websocket, request, message, host, port)

        log.info('Closing connection from {}:{}'.format(host, port))
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        log.error(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

# Main
if __name__ == '__main__':
    async def login(request):
        return web.FileResponse("./webpages/index.html")

    log.info('Starting web application')
    app = web.Application()
    log.info('Adding routes')
    app.add_routes([web.get('/server', websocket_handler),
                    web.get('/', login),
                    web.static('/static', './webpages')])

    log.info("Fetching SSL certificates.")
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    localhost_cert = os.path.relpath(cl.get('ssl_cert'))
    localhost_key = os.path.relpath(cl.get('ssl_key'))
    ssl_context.load_cert_chain(localhost_cert, keyfile=localhost_key)

    log.info("Starting webserver.")
    web.run_app(app, ssl_context = ssl_context)