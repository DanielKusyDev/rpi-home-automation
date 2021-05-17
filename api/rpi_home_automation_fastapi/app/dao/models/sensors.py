import enum
from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Table, Unicode, UniqueConstraint)
from sqlalchemy_utils import ChoiceType

from app.dao import metadata


class SensorTypeEnum(enum.Enum):
    MOISTURE = "MOISTURE_SENSOR"
    TEMPERATURE = "TEMPERATURE_SENSOR"
    SUNLIGHT_LEVEL = "SUNLIGHT_LEVEL_SENSOR"


sensor_type = Table(
    "SensorType",
    metadata,
    Column("Id", Integer, primary_key=True),
    Column("Name", ChoiceType(SensorTypeEnum, impl=Unicode(255)), nullable=False, unique=True),
    Column("Description", Unicode(255)),
)

sensor = Table(
    "Sensor",
    metadata,
    Column("Id", Integer, primary_key=True),
    Column("PlantId", Integer, ForeignKey("Plant.Id")),
    Column("SensorTypeId", Integer, ForeignKey("SensorType.Id")),
    Column("GpioChannel", Integer, ForeignKey("Gpio.Channel"), unique=True),
    Column("Description", Unicode(255), nullable=True, unique=False),
    Column("AddDate", DateTime, default=datetime.utcnow),
    UniqueConstraint('PlantId', 'SensorTypeId', name='UQ__SensorTypeId__PlantId')
)
