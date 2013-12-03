import unittest

from messagebus.util import date_time_utils
from messagebus import Message

class TestMessage(unittest.TestCase):

    def setUp(self):
        date_time_utils.set_fixed_timestamp(100)

    def tearDown(self):
        date_time_utils.set_use_system_timestamp()

    def test_constructor(self):

        message = Message(type="type", source="source", timestamp=1000, data={"foo":"bar"})
        self.assertEquals("source", message.source)
        self.assertEquals("type", message.type)
        self.assertEquals(1000, message.timestamp)
        self.assertEquals({"foo":"bar"}, message.data)


if __name__ == '__main__':
    unittest.main()