from app.config.settings import (DB_DRIVER, DB_HOST, DB_NAME, DB_PASSWORD,
                                 DB_PORT, DB_USER)
from sqlalchemy import MetaData, create_engine

SQLALCHEMY_DATABASE_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

database = create_engine(SQLALCHEMY_DATABASE_URL)

metadata = MetaData(
    naming_convention={
        "ix": "IX__%(table_name)s__%(column_0_N_name)s",
        "uq": "UQ__%(table_name)s__%(column_0_N_name)s",
        "ck": "CK__%(table_name)s__%(constraint_name)s",
        "fk": "FK__%(table_name)s__%(column_0_N_name)s__%(referred_table_name)s",
        "pk": "PK__%(table_name)s",
    },
)


def init_database() -> None:
    import app.dao.models.gpio
    import app.dao.models.plants
    import app.dao.models.sensors

    metadata.bind = create_engine(SQLALCHEMY_DATABASE_URL)


async def truncate_database() -> None:
    await database.execute("""TRUNCATE {} RESTART IDENTITY""".format(",".join(f'"{table.name}"' for table in reversed(metadata.sorted_tables))))


init_database()
