import asyncio
from dataclasses import dataclass
from os import environ
from time import sleep

import RPi.GPIO as GPIO

CHANNELS = [17, 27]
DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")
DB_USER = environ.get("DB_USER")
DB_PASSWORD = environ.get("DB_PASSWORD")
DB_NAME = environ.get("DB_NAME")


@dataclass
class Message:
    VAL: int
    SNSR: int
    EOM: int
    TYP: str = "ANL"

    def marshal(self) -> str:
        return f"TYP:{self.TYP}\r\nVAL:{self.VAL}\r\nSNSR:{self.SNSR}\r\nEOM:{self.EOM}\r\n"

    def encode(self) -> bytes:
        return self.marshal().encode()


def set_gpio():
    GPIO.setmode(GPIO.BCM)
    for channel in CHANNELS:
        GPIO.setup(channel, GPIO.IN)


async def main():
    set_gpio()
    while True:
        reader, writer = await asyncio.open_connection("127.0.0.1", 1225)
        for channel in CHANNELS[:-1]:
            message = Message(int(GPIO.input(channel)), channel, 0)
            print(message)
            writer.write(message.encode())
            print(await reader.read(1000))

        message = Message(int(GPIO.input(CHANNELS[-1])), CHANNELS[-1], 1)
        writer.write(message.encode())
        print(await reader.read(1000))

        writer.close()

        sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
