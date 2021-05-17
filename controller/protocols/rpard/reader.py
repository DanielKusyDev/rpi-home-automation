from dao import engine
from dao.models import sensor
from protocols.rpard.message import HandlerChain, Message, Response


class RpardReader:
    def read(self, data: bytes) -> Message:
        message = Message()
        for line in data.decode().split("\r\n"):
            if line == "":
                break
            message = HandlerChain(message)(line)

        return message

    def process_request(self, message: Message) -> Response:
        print(engine.execute(sensor.select().where(sensor.c.id == message.sensor_id)).fetchone())
        return Response(code=1)
