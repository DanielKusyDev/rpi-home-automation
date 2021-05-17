import asyncio
from asyncio import StreamReader, StreamWriter

from config import *
from protocols.common import InputError
from protocols.rpard.message import Response
from protocols.rpard.reader import RpardReader
from protocols.rpard.writer import RpardWriter


async def handle_connection(raw_reader: StreamReader, raw_writer: StreamWriter):
    addr = raw_writer.get_extra_info("peername")
    logger.info(f"ESTABLISHED: {addr}")

    data = await raw_reader.read(1024)
    reader = RpardReader()
    writer = RpardWriter(raw_writer)
    try:
        message = reader.read(data)
    except InputError as e:
        response = Response(code=0, description=str(e))
    else:
        response = reader.process_request(message)

    writer.write(response)

    await raw_writer.drain()
    raw_writer.close()


async def main():
    port = environ.get("CONTROLLER_PORT", 1225)
    server = await asyncio.start_server(handle_connection, "0.0.0.0", port)
    addr = server.sockets[0].getsockname()
    logger.info(f"Serving on {addr}")

    async with server:
        await server.serve_forever()


asyncio.run(main())
