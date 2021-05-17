from sqlalchemy import Boolean, Column, DateTime, Integer, Table, Unicode

from dao import metadata

sensor = Table(
    "sensors_sensor",
    metadata,
    Column("id", Integer),
    Column("description", Unicode(255)),
    Column("state", Boolean),
    Column("device_id", Integer),
    Column("plant_id", Integer),
    Column("sensor_type_id", Integer),
)
