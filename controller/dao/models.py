from sqlalchemy import Boolean, Column, Float, Integer, String, Table, Unicode

from dao import metadata

sensor = Table(
    "sensors_sensor",
    metadata,
    Column("id", Integer),
    Column("description", Unicode(255)),
    Column("analog_output", Boolean, nullable=True),
    Column("digital_output", Float, nullable=True),
    Column("device_id", Integer),
    Column("plant_id", Integer),
    Column("sensor_type_id", Integer),
)

device = Table(
    "sensors_device",
    metadata,
    Column("id", Integer),
    Column("name", Unicode(15)),
    Column("mac_address", String(12)),
)

cli = Table(
    "sensors_cli",
    metadata,
    Column("sensor_id", Integer),
    Column("module", String(255)),
    Column("name", String(255)),
    Column("parameters", String(511)),
)
