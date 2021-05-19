import asyncio
from asyncio import StreamReader, StreamWriter
from importlib import import_module

from config import *
from dao import engine
from dao.crud import (fetch_device, fetch_sensor_with_given_id_and_device,
                      update_sensor_state)
from dao.models import cli
from dao.utils import row_to_dict
from protocols.common import InputError
from protocols.rpard.domain import Code, Message, Response
from protocols.rpard.reader import RpardReader
from protocols.rpard.writer import RpardWriter


def run_request(message: Message, hostname: str) -> Response:
    def call_cli(sensor_id: int) -> Code:
        row = engine.execute(cli.select().where(cli.c.sensor_id == sensor_id)).fetchone()
        if row:
            row = row_to_dict(row)
            try:
                module = import_module(row.get("module"), ".")
            except ModuleNotFoundError:
                logger.exception(f"Module not found for row {row}")
                return Code.UNKNOWN_ERROR

            name = row.get("name")
            try:
                params_from_db = row.get("parameters").replace(", ", ",").replace('"', "").split(",")
                kwargs = dict([param.split("=") for param in params_from_db])
                getattr(module, name)(**kwargs)
            except Exception as e:
                logger.exception(f"Exception thrown at {module}:{name}. EXC: {e}")

        return Code.SUCCESS

    fetched_device = fetch_device(hostname)
    if fetched_device is None:
        return Response(Code.PERMISSION_ERROR)

    if fetch_sensor_with_given_id_and_device(message.sensor_id, row_to_dict(fetched_device)["id"]) is None:
        return Response(Code.NOT_FOUND_ERROR)

    update_sensor_state(message)
    return Response(call_cli(sensor_id=message.sensor_id))


async def handle_connection(raw_reader: StreamReader, raw_writer: StreamWriter):
    addr = raw_writer.get_extra_info("peername")
    logger.info(f"ESTABLISHED: {addr}")
    data = await raw_reader.read(1024)
    reader = RpardReader()
    writer = RpardWriter(raw_writer)
    try:
        message = reader.read(data)
    except InputError:
        response = Response(code=Code.INPUT_VALIDATION_ERROR)
    else:
        response = run_request(message, addr[0])

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
