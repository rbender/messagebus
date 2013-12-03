import unittest

from messagebus.util import ToStringBuilder

class TestMessage(unittest.TestCase):

    def test_to_string(self):
        builder = ToStringBuilder("MyClass")
        builder.append("foo", "bar").append("hello", "world")
        s = builder.to_string()

        self.assertEquals("MyClass[foo=bar,hello=world]", s)
