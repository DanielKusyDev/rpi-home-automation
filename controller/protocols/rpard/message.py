import abc
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from protocols.common import InputError


@dataclass
class Response:
    code: int
    description: str = ""


class MessageType(Enum):
    DIGITAL = "DGT"
    ANALOG = "ANL"


class Message:
    type_: MessageType
    value: float
    sensor_id: int


class MessageHandler(abc.ABC):
    message: Optional[Message] = None
    _next: Optional["MessageHandler"] = None

    def __init__(self, message: Message):
        self.message = message

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class ValueHandler(MessageHandler):
    _next = None

    def __call__(self, field: str, value: str) -> Message:
        if field == "VAL":
            if self.message.type_ == MessageType.ANALOG:
                try:
                    self.message.value = int(value)
                    if self.message.value not in (1, 0):
                        raise ValueError
                except ValueError:
                    raise InputError("Message's value with type of ANL must be one of 0, 1")
            else:
                self.message.value = float(value)
        return self.message


class TypeHandler(MessageHandler):
    _next = ValueHandler

    def __call__(self, field: str, value: str) -> Message:
        if field == "TYP":
            if value == MessageType.ANALOG.value:
                self.message.type_ = MessageType.ANALOG
            elif value == MessageType.DIGITAL.value:
                self.message.type_ = MessageType.DIGITAL
            else:
                raise ValueError("Given TYP is incorrect. Must be one of (%s, %s)", MessageType.ANALOG.value, MessageType.DIGITAL.value)
            return self.message
        return self._next(self.message)(field, value)


class SensorHandler(MessageHandler):
    _next = TypeHandler

    def __call__(self, field: str, value: str) -> Message:
        if field == "SNSR":
            try:
                self.message.sensor_id = int(value)
            except ValueError:
                raise InputError("SNSR must be an integer")
        return self._next(self.message)(field, value)


class HandlerChain(MessageHandler):
    _next = SensorHandler

    def __call__(self, data: str) -> Message:
        field, value = data.split(":")
        if not value:
            raise InputError("Missing data. All fields are required.")
        return self._next(self.message)(field, value)
