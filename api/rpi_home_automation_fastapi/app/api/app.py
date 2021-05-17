from app.api.errors import validation_error_handler
from app.api.routes import register_routers
from app.config import settings
from app.config.settings import DEBUG
from app.dao import database
from fastapi.applications import FastAPI
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware
from toolz import pipe


async def connect_database():
    database.connect()


async def disconnect_database():
    database.disconnect()


async def initialize_gpio():
    # pins = get_gpio_pins()
    # GPIO.setmode(GPIO_MODE)
    # for gpio in pins:
    #     if gpio.channel not in GPIO_AVAILABLE_PINS:
    #         logging.error(f"GPIO PIN #{gpio.channel} IS INVALID")
    #         exit(1)
    #     if gpio.callback:
    #         callback = get_gpio_callback(gpio)
    #         GPIO.setup(gpio.channel, GPIO.IN)
    #         GPIO.add_event_detect(gpio.channel, GPIO.BOTH, bouncetime=300)
    #         GPIO.add_event_callback(gpio.channel, callback)
    pass


def create_instance() -> FastAPI:
    return FastAPI(debug=settings.DEBUG, title=settings.PROJECT_NAME)


def register_events(app: FastAPI) -> FastAPI:
    app.on_event("startup")(connect_database)
    if not DEBUG:
        app.on_event("startup")(initialize_gpio)
    app.on_event("shutdown")(disconnect_database)

    return app


def register_middlewares(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def register_exception_handlers(app: FastAPI) -> FastAPI:
    app.add_exception_handler(ValidationError, validation_error_handler)
    return app


def init_app() -> FastAPI:
    app = create_instance()
    app = pipe(
        app,
        register_events,
        register_middlewares,
        register_exception_handlers,
        register_routers,
    )
    return app
