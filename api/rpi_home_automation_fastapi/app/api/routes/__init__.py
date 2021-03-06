from app.api.routes import root, weather
from app.config.settings import API_PREFIX
from fastapi import APIRouter, FastAPI


def register_routers(app: FastAPI) -> FastAPI:
    router = APIRouter()
    router.include_router(root.router)
    router.include_router(weather.router, tags=["Weather"])
    app.include_router(router, prefix=API_PREFIX)
    return app
