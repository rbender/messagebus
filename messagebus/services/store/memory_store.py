"""
Basic implementaiton of a MessageStore that keeps messages in an
in-memory dictionary. Useful for testing but not best for
real usage since it will grow unbounded.
"""

import logging

from message_store import MessageStore
from collections import OrderedDict

class MemoryMessageStore(MessageStore):

    def __init__(self):
        self.logger = logging.getLogger("MemoryMessageStore")
        self.logger.debug("Instantiated MemoryMessageStore")
        self.messages = OrderedDict()

    def save_message(self, message):
        self.logger.debug("Save message {}".format(message))
        self.messages[message.id] = message

    def load_message(self, id):
        self.logger.debug("Load message {}".format(id))
        return self.messages[id]

    def filter_messages(self, message_filter):
        self.logger.debug("Filter Messages")
        return filter(message_filter, self.messages.values())

