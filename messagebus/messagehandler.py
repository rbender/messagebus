

class MessageHandler:

    def handle(self, message):
        pass

class FunctionMessageHandler(MessageHandler):
    """
    Simple MessageHandler that wraps a function
    """

    def __init__(self, function):
        self.function = function

    def handle(self, message):
        self.function(message)
