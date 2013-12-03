
import logging


class MessageSubscription:

    def __init__(self, message_filter, listener):
        self.logger = logging.getLogger("MessageSubscription")
        self.message_filter = message_filter
        self.listener = listener

    def match(self, message):
        return self.message_filter.match(message)

    def handle(self, message):
        self.listener.handle(message)



