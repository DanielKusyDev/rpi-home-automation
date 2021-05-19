from sqlalchemy import func, update
from sqlalchemy.engine import RowProxy

from dao import engine
from dao.models import device, sensor
from protocols.rpard.domain import Message, MessageType
from utils import get_mac_address


def update_sensor_state(message: Message) -> None:
    if message.type_ == MessageType.ANALOG:
        values_to_update = dict(analog_output=bool(int(message.value)))
    else:
        values_to_update = dict(digital_output=message.value)

    with engine.begin() as conn:
        conn.execute(update(sensor).where(sensor.c.id == message.sensor_id).values(**values_to_update))


def fetch_sensor_with_given_id_and_device(sensor_id: int, device_id: int) -> RowProxy:
    with engine.begin() as conn:
        row = conn.execute(sensor.select().where(sensor.c.id == sensor_id)).fetchone()

    return row


def fetch_device(hostname: str):
    with engine.begin() as conn:
        row = conn.execute(device.select().where(func.lower(device.c.mac_address).in_((get_mac_address(), get_mac_address(hostname))))).fetchone()

    return row
