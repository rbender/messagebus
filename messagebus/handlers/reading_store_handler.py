"""
MessageListener implementation that saves reading messages to a data store.
"""
from messagebus import MessageHandler

class ReadingStoreHandler(MessageHandler):

    def __init__(self, reading_store):
        self.reading_store = reading_store

    def handle(self, message):
        self.reading_store.save_reading(message)