import asyncio
from asyncio import StreamReader, StreamWriter
from importlib import import_module

from dotenv import load_dotenv

from config import *
from dao import engine
from dao.crud import fetch_device, fetch_sensor_with_given_device_specific_id, update_sensor_state
from dao.models import cli
from dao.utils import row_to_dict
from protocols.common import InputError
from protocols.rpard.domain import Code, Message, Response
from protocols.rpard.reader import RpardReader
from protocols.rpard.writer import RpardWriter

load_dotenv()
SERVER_HOST = environ.get("SERVER_HOST")
SERVER_PORT = environ.get("SERVER_PORT")


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
    fetched_device = row_to_dict(fetched_device)
    fetched_sensor = fetch_sensor_with_given_device_specific_id(message.device_specific_id, fetched_device["id"])
    if fetched_sensor is None:
        return Response(Code.NOT_FOUND_ERROR)

    fetched_sensor = row_to_dict(fetched_sensor)
    update_sensor_state(message)
    return Response(call_cli(sensor_id=fetched_sensor["id"]))


async def handle_connection(raw_reader: StreamReader, raw_writer: StreamWriter):
    addr = raw_writer.get_extra_info("peername")
    logger.info(f"ESTABLISHED: {addr}")
    reader = RpardReader()
    writer = RpardWriter(raw_writer)
    last_message = False
    while not last_message:
        data = await raw_reader.read(1024)
        try:
            message = reader.read(data)
            logger.info(message)
        except InputError as e:
            response = Response(code=Code.INPUT_VALIDATION_ERROR)
            last_message = True
        else:
            response = run_request(message, addr[0])
            last_message = message.last_message
        writer.write(response)
        await raw_writer.drain()

    raw_writer.close()


async def main():
    server = await asyncio.start_server(handle_connection, SERVER_HOST, SERVER_PORT)
    addr = server.sockets[0].getsockname()
    logger.info(f"Serving on {addr}")

    async with server:
        await server.serve_forever()


asyncio.run(main())
