import util.pattern_matching as pattern_matching

class PatternMatcher:
    """ Interface for matching text patterns"""

    def match(self, value):
        return False

class SimplePatternMatcher(PatternMatcher):
    """ Pattern matcher that uses simple wildcard (*) matching """

    def __init__(self, pattern):
        self._pattern = pattern
        self._regex = pattern_matching.expand_regex(pattern)

    def match(self, value):
        return self._regex.match(value)

    def __str__(self):
        return self._pattern

class AllMatcher(PatternMatcher):
    """ Always matches (returns true) """

    def match(self, value):
        return True

    def __str__(self):
        return "*"

class MessageFilter:

    def match(self, message):
        return False

class PatternMessageFilter(MessageFilter):

    def __init__(self, **kwargs):
        self.type = kwargs.get("type", "*")
        self.source = kwargs.get("source", "*")
        self.target = kwargs.get("target", "*")
        self._type_matcher = self.__build_matcher(self.type)
        self._source_matcher = self.__build_matcher(self.source)
        self._target_matcher = self.__build_matcher(self.target)

    def __build_matcher(self, pattern):

        if pattern == "*":
            return AllMatcher()
        else:
            return SimplePatternMatcher(pattern)

    def match(self, message):
        return self._match_type(message) and self._match_source(message) and self._match_target(message)

    def _match_type(self, message):
        return self._type_matcher.match(message.type)

    def _match_source(self, message):
        return self._source_matcher.match(message.source)

    def _match_target(self, message):
        return message.target is None or self._target_matcher.match(message.target)

    def __call__(self, *args, **kwargs):
        return self.match(args[0])

    def __str__(self):
        return "PatternFilter(type=%s, source=%s, target=%s)" % (self._type_matcher, self._source_matcher, self._target_matcher)


class AllMessageFilter(MessageFilter):
    """
    MessageFilter that lets all messages through
    """

    def match(self, message):
        return True
