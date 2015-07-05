"""
MessageListener implementation that saves messages to a MessageStore.
"""
from messagebus import MessageHandler

class MessageStoreHandler(MessageHandler):

    def __init__(self, message_store):
        self.message_store = message_store

    def handle(self, message):
        self.message_store.save_message(message)