from datetime import datetime

from app.dao import metadata
from sqlalchemy import Column, DateTime, Integer, Table, Unicode

plant = Table(
    "Plant",
    metadata,
    Column("Id", Integer, primary_key=True),
    Column("Name", Unicode(255), nullable=False, unique=True),
    Column("Description", Unicode(512), nullable=True, unique=False),
    Column("Image", Unicode(512), nullable=True, unique=False),
    Column("AddDate", DateTime, default=datetime.utcnow),
)
