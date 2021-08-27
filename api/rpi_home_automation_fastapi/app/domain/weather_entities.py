from app.domain import Entity


class Weather(Entity):
    description: str
    icon: str
    temperature: float
    pressure: int
    humidity: int
