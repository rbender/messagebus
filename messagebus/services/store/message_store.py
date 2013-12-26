"""
Interface for storing messages for later retrieval and querying. This class
can also be used as a dummy implementation that throws messages away
"""

class MessageStore:

    def save_message(self, message):
        pass

    def load_message(self, id):
        return None
