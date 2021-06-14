from dao import engine
from dao.models import device, sensor
from protocols.rpard.domain import Message, MessageType
from sqlalchemy import func, update
from utils import get_mac_address
from config import logger


def update_sensor_state(message: Message) -> None:
    if message.type_ == MessageType.ANALOG:
        values_to_update = dict(analog_output=bool(int(message.value)))
    else:
        values_to_update = dict(digital_output=message.value)

    with engine.begin() as conn:
        conn.execute(update(sensor).where(sensor.c.device_specific_id == message.device_specific_id).values(**values_to_update))


def fetch_sensor_with_given_device_specific_id(device_specific_id: str, device_id: int):
    with engine.begin() as conn:
        row = conn.execute(sensor.select().where(sensor.c.device_specific_id == device_specific_id).where(sensor.c.device_id == device_id)).fetchone()

    return row


def fetch_device(hostname: str):
    with engine.begin() as conn:
        mac_address = get_mac_address(ip=hostname)
        row = conn.execute(device.select().where(func.lower(device.c.mac_address) == mac_address)).fetchone()

    return row
