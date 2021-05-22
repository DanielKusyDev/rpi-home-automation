from os import environ

from dotenv import load_dotenv
from loguru import logger

logger.add(f"logs/info.log", format="{time} {level} {message}", level="INFO", rotation="500 MB")

load_dotenv()

SERVER_HOST = environ.get("SERVER_HOST")
SERVER_PORT = environ.get("SERVER_PORT")
DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")
DB_USER = environ.get("DB_USER")
DB_PASSWORD = environ.get("DB_PASSWORD")
DB_NAME = environ.get("DB_NAME")
DB_DRIVER = environ.get("DB_DRIVER")
