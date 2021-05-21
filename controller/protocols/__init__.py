import abc


class ProtocolInterface(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def read(cls, data: bytes, *args, **kwargs):
        raise NotImplemented

    @classmethod
    @abc.abstractmethod
    def write(cls):
        raise NotImplemented
