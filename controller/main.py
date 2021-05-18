import asyncio
from asyncio import StreamReader, StreamWriter
from typing import Optional

import getmac as gm
from sqlalchemy import func

from config import *
from dao import engine
from dao.models import device
from dao.utils import row_to_dict
from protocols.common import InputError
from protocols.rpard.message import Response
from protocols.rpard.reader import RpardReader
from protocols.rpard.writer import RpardWriter


def get_mac_address(*args, **kwargs) -> Optional[str]:
    mac_with_colons = gm.get_mac_address(*args, **kwargs)
    if mac_with_colons:
        return mac_with_colons.lower().replace(":", "").replace("-", "")
    return mac_with_colons


def validate_device(addr: str) -> int:
    this_mac = get_mac_address()
    incoming_mac = get_mac_address(addr)
    row = engine.execute(device.select().where(func.lower(device.c.mac_address).in_((this_mac, incoming_mac)))).fetchone()
    if row:
        return row_to_dict(row)["id"]
    else:
        raise PermissionError("Given host is not permitted.")


async def handle_connection(raw_reader: StreamReader, raw_writer: StreamWriter):
    addr = raw_writer.get_extra_info("peername")
    logger.info(f"ESTABLISHED: {addr}")
    data = await raw_reader.read(1024)
    reader = RpardReader()
    writer = RpardWriter(raw_writer)
    try:
        device_id = validate_device(addr[0])
        message = reader.read(data)
    except (InputError, PermissionError) as e:
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
