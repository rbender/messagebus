from messagebus import MessageHandler

class MockMessageHandler(MessageHandler):

    def __init__(self):
        self.message = None

    def handle(self, message):
        self.message = message
