from app.api.routes import gpios, plants, root, sensors
from app.config.settings import API_PREFIX
from fastapi import APIRouter, FastAPI


def register_routers(app: FastAPI) -> FastAPI:
    router = APIRouter()
    router.include_router(root.router, prefix="")
    router.include_router(plants.router, tags=["plants"])
    router.include_router(sensors.router, tags=["sensors"])
    router.include_router(gpios.router, tags=["gpios"])
    app.include_router(router, prefix=API_PREFIX)
    return app
