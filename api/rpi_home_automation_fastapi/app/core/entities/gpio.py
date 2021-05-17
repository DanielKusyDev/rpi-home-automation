from app.core.entities import Model


class Gpio(Model):
    channel: int
    state: bool
