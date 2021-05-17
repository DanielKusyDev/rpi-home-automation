from app.dao import metadata
from sqlalchemy import Boolean, Column, Integer, String, Table

gpio = Table(
    "Gpio",
    metadata,
    Column("Channel", Integer, primary_key=True),
    Column("State", Boolean, nullable=True),
    Column("Callback", String(255), nullable=True),
)
