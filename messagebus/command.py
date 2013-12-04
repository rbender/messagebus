from message import Message

class Command(Message):

    def __init__(self, **kwargs):
        Message.__init__(self, category="command", **kwargs)
