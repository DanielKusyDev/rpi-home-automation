from sqlalchemy import MetaData, create_engine

from config import DB_DRIVER, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

SQLALCHEMY_DATABASE_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()


def init_database() -> None:
    metadata.bind = create_engine(SQLALCHEMY_DATABASE_URL)


async def truncate_database() -> None:
    await engine.execute("""TRUNCATE {} RESTART IDENTITY""".format(",".join(f'"{table.name}"' for table in reversed(metadata.sorted_tables))))


init_database()
