from app.api.errors import validation_error_handler
from app.api.routes import register_routers
from app.config import settings
from fastapi.applications import FastAPI
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware
from toolz import pipe


def create_instance() -> FastAPI:
    return FastAPI(debug=settings.DEBUG, title=settings.PROJECT_NAME)


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
        register_middlewares,
        register_exception_handlers,
        register_routers,
    )
    return app
