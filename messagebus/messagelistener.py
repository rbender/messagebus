

class MessageListener:

    def handle(self, message):
        pass

class FunctionMessageListener(MessageListener):
    """
    Simple MessageListener that wraps a function
    """

    def __init__(self, function):
        self.function = function

    def handle(self, message):
        self.function(message)
