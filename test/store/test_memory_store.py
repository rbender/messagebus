import unittest

from messagebus.store import MemoryMessageStore
from messagebus import Event
from messagebus.messagefilter import PatternMessageFilter

class TestMemoryStore(unittest.TestCase):

    def setUp(self):
        self.store = MemoryMessageStore()

    def test_save_and_load(self):

        message = Event(id=10, source="foo", type="bar")
        self.store.save_message(message)

        self.assertEquals(message, self.store.load_message(10))

    def test_filter_messages(self):
        message1 = Event(id=10, source="foo", type="bar")
        message2 = Event(id=20, source="foo", type="baz")

        self.store.save_message(message1)
        self.store.save_message(message2)

        message_filter = PatternMessageFilter(source="foo", type="baz")
        messages = self.store.filter_messages(message_filter)

        self.assertEquals(1, len(messages))
        self.assertEquals(message2, messages[0])
