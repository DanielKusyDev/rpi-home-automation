from protocols.rpard.domain import HandlerChain, Message


class RpardReader:
    def read(self, data: bytes) -> Message:
        message = Message()
        for line in data.decode().split("\r\n"):
            if line == "":
                break
            message = HandlerChain(message)(line)

        return message
