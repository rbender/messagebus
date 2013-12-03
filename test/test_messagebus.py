import unittest
import dummy_threading

from messagebus import Message
from messagebus import PatternMessageFilter
from messagebus import MessageBus

from mock import MockMessageListener
from mock import MockMessageFilter

class TestMessageBus(unittest.TestCase):

    def setUp(self):
        self.bus = MessageBus()
        self.bus._thread_constructor = dummy_threading.Thread

    def test_subscribe(self):
        pass

    def test_send_message_calls_subscriber_when_filter_matches(self):

        listener = MockMessageListener()
        message_filter = MockMessageFilter(True)
        self.bus.subscribe(listener, message_filter)

        message = Message(type="foo", source="bar")
        self.bus.send_message(message)

        self.assertEquals(message, message_filter.message)
        self.assertEquals(message, listener.message)

    def test_send_message_does_not_call_subscriber_when_filter_does_not_match(self):

        listener = MockMessageListener()
        message_filter = MockMessageFilter(False)
        self.bus.subscribe(listener, message_filter)

        message = Message(type="foo", source="bar")
        self.bus.send_message(message)

        self.assertEquals(message, message_filter.message)
        self.assertIsNone(listener.message)

if __name__ == '__main__':
    unittest.main()