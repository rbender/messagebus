from messagebus import MessageListener

class MockMessageListener(MessageListener):

    def __init__(self):
        self.message = None

    def handle(self, message):
        self.message = message
