import abc
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from protocols.common import InputError


class Code(int, Enum):
    SUCCESS = 0
    UNKNOWN_ERROR = 1
    PERMISSION_ERROR = 2
    INPUT_VALIDATION_ERROR = 3
    NOT_FOUND_ERROR = 4


@dataclass
class Response:
    code: Code


class MessageType(Enum):
    DIGITAL = "DGT"
    ANALOG = "ANL"


class Message:
    type_: MessageType
    value: float
    device_specific_id: str
    last_message: bool

    def __str__(self):
        return f"TYP:{self.type_} VAL:{self.value} SNSR:{self.device_specific_id} EOM:{int(self.last_message)}"


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
            self.message.device_specific_id = value
        return self._next(self.message)(field, value)


class EndOfMessageHandler(MessageHandler):
    _next = SensorHandler

    def __call__(self, field: str, value: str) -> Message:
        if field == "EOM":
            try:
                self.message.last_message = bool(int(value))
                if int(value) not in [0, 1]:
                    raise ValueError
            except ValueError:
                raise InputError("EOM must be a 0/1 value (int)")
        return self._next(self.message)(field, value)


class HandlerChain(MessageHandler):
    _next = EndOfMessageHandler

    def __call__(self, data: str) -> Message:
        field, value = data.split(":")
        if not value:
            raise InputError("Missing data. All fields are required.")
        return self._next(self.message)(field, value)
