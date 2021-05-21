import asyncio
from dataclasses import dataclass
from os import environ
from time import sleep

from dotenv import load_dotenv

import RPi.GPIO as GPIO

load_dotenv()
CHANNELS = [17, 27]

SERVER_HOST = environ.get("SERVER_HOST")
SERVER_PORT = environ.get("SERVER_PORT")
SAMPLING_FREQ = environ.get("SAMPLING_FREQ", 60)


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
        reader, writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)
        for channel in CHANNELS[:-1]:
            message = Message(int(GPIO.input(channel)), channel, 0)
            print(message)
            writer.write(message.encode())
            print(await reader.read(1000))

        message = Message(int(GPIO.input(CHANNELS[-1])), CHANNELS[-1], 1)
        writer.write(message.encode())
        print(await reader.read(1024))

        writer.close()

        sleep(SAMPLING_FREQ)


if __name__ == "__main__":
    asyncio.run(main())
