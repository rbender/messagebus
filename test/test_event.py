import unittest

from messagebus.util import date_time_utils
from messagebus import Event

class TestEvent(unittest.TestCase):

    def setUp(self):
        date_time_utils.set_fixed_timestamp(100)

    def tearDown(self):
        date_time_utils.set_use_system_timestamp()

    def test_constructor(self):

        event = Event(type="type", source="source", timestamp=1000, data={"foo":"bar"})
        self.assertEquals("source", event.source)
        self.assertEquals("type", event.type)
        self.assertEquals(1000, event.timestamp)
        self.assertEquals({"foo":"bar"}, event.data)
        self.assertEquals("event", event.category)


if __name__ == '__main__':
    unittest.main()
