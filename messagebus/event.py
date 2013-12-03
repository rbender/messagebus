from message import Message

class Event(Message):

    def __init__(self, **kwargs):
        Message.__init__(self, **kwargs)
        self.category = "event"
