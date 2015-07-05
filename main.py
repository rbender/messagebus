import logging

from messagebus import Message
from messagebus import PatternMessageFilter
from messagebus import FunctionMessageHandler
from messagebus import MessageBus


def handle(message):
    logging.info("Handled {}".format(message))

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    bus = MessageBus()

    listener = FunctionMessageHandler(handle)

    bus.subscribe(listener, PatternMessageFilter("foo", "bar"))

    message = Message(type="foo", source="bar", timestamp=1000, data={"a":"b"})
    bus.send_message(message)

    logging.info("Done")
