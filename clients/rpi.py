import asyncio
from dataclasses import dataclass
from os import environ
from time import sleep

import RPi.GPIO as GPIO
import psycopg2
from psycopg2._psycopg import connection

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
    TYP: str = "ANL"

    def marshal(self) -> str:
        return f"TYP:{self.TYP}\r\nVAL:{self.VAL}\r\nSNSR:{self.SNSR}\r\n"

    def encode(self) -> bytes:
        return self.marshal().encode()


def set_gpio():
    GPIO.setmode(GPIO.BCM)
    for channel in CHANNELS:
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel, GPIO.LOW)


async def main():
    set_gpio()
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    while True:
        reader, writer = await asyncio.open_connection("127.0.0.1", 1225)
        for channel in CHANNELS:
            message = Message(GPIO.input(channel), channel)
            writer.write(message.encode())
            await reader.read(1000)

        writer.close()
        sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
