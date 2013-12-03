from messagebus import MessageFilter

class MockMessageFilter(MessageFilter):

    def __init__(self, matches=True):
        self.message = None
        self._matches = matches

    def match(self, message):
        self.message = message
        return self._matches
