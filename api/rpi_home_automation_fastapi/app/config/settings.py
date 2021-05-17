import logging
import os
import sys
from pathlib import Path

from app.config.logging import InterceptHandler
from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret

API_PREFIX = "/api"
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
if not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)


cfg = Config()

# ENVS
HOST: str = cfg("HOST", cast=str, default="0.0.0.0")
PORT: int = cfg("PORT", cast=int, default=8000)
DEBUG: bool = cfg("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = cfg("SECRET_KEY", cast=Secret)
PROJECT_NAME: str = cfg("PROJECT_NAME", cast=str, default="Plants control")
DB_HOST = cfg("DB_HOST", cast=str)
DB_PORT = cfg("DB_PORT", cast=int)
DB_USER = cfg("DB_USER", cast=str, default="")
DB_PASSWORD = cfg("DB_PASSWORD", cast=str, default="")
DB_NAME = cfg("DB_NAME", cast=str)
DB_DRIVER = cfg("DB_DRIVER", cast=str)
RPI_ENABLED = cfg("RPI_ENABLED", cast=bool)
BASE_URL = cfg("BASE_URL", cast=str, default=f"http://{HOST}:{PORT}{API_PREFIX}")

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access", "gunicorn.error")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

# Api
DEFAULT_PAGINATION_SIZE = 50

# RPi
if RPI_ENABLED:
    import RPi.GPIO as GPIO

    GPIO_MODE = GPIO.BCM
else:
    GPIO_MODE = 0
GPIO_AVAILABLE_PINS = [5, 6, 16, 17, 22, 23, 24, 25, 26, 27]
