from unittest import TestCase

from messagebus import Message
from messagebus import PatternMessageFilter


class TestPatternMessageFilter(TestCase):

    def test_match_true(self):

        message = Message(type="foo.hello.bar.world", source="source")

        filter = PatternMessageFilter("foo.*.bar.*", "*")
        self.assertTrue(filter.match(message))

    def test_match_fails_on_type(self):

        message = Message(type="foo.hello.baz.world", source="source")

        filter = PatternMessageFilter("foo.*.bar.*", "*")
        self.assertFalse(filter.match(message))
