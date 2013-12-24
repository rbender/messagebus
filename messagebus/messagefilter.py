import util.pattern_matcher as pattern_matcher

class MessageFilter:

    def match(self, message):
        return False

class PatternMessageFilter(MessageFilter):

    def __init__(self, type, source):
        self.type = type
        self.source = source
        self._type_regex = pattern_matcher.expand_regex(type)
        self._source_regex = pattern_matcher.expand_regex(source)

    def match(self, message):
        return self._type_regex.match(message.type) and self._source_regex.match(message.source)

    def __call__(self, *args, **kwargs):
        return self.match(args[0])

class AllMessageFilter(MessageFilter):
    """
    MessageFilter that lets all messages through
    """

    def match(self, message):
        return True
