from asyncio import StreamWriter
from dataclasses import dataclass
from typing import Union

from protocols.rpard.domain import Response


@dataclass(frozen=True)
class RpardWriter:
    _writer: StreamWriter

    @staticmethod
    def _construct_payload(field: str, value: Union[str, float, int]):
        return f"{field}:{value}\r\n"

    def write(self, response: Response) -> None:
        data = self._construct_payload("CODE", response.code)
        self._writer.write(data.encode())
