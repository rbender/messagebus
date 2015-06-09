from unittest import TestCase

from messagebus import Message, Command
from messagebus.messagefilter import PatternMessageFilter, AllMatcher, SimplePatternMatcher

class TestPatternMatcher(TestCase):

    def test_all_matcher(self):

        matcher = AllMatcher()
        self.assertTrue(matcher.match("foo"))

    def test_simple_pattern_matcher(self):

        matcher = SimplePatternMatcher("foo.*")
        self.assertTrue(matcher.match("foo.bar"))
        self.assertFalse(matcher.match("fo.bar"))


class TestPatternMessageFilter(TestCase):

    def test_match_true(self):

        message = Message(type="foo.hello.bar.world", source="source")

        filter = PatternMessageFilter(type="foo.*.bar.*", source="*")
        self.assertTrue(filter.match(message))

    def test_match_fails_on_type(self):

        message = Message(type="foo.hello.baz.world", source="source")

        filter = PatternMessageFilter(type="foo.*.bar.*", source="*")
        self.assertFalse(filter.match(message))

    def test_match_target(self):

        message = Command(type="foo", source="bar", target="baz")
        filter = PatternMessageFilter(target="*")
        self.assertTrue(filter.match(message))
