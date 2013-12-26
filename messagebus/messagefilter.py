import util.pattern_matcher as pattern_matcher

class MessageFilter:

    def match(self, message):
        return False

class PatternMessageFilter(MessageFilter):

    def __init__(self, **kwargs):
        self.type = kwargs.get("type", "*")
        self.source = kwargs.get("source", "*")
        self.target = kwargs.get("target", "*")
        self._type_regex = pattern_matcher.expand_regex(self.type)
        self._source_regex = pattern_matcher.expand_regex(self.source)
        self._target_regex = pattern_matcher.expand_regex(self.target)

    def match(self, message):
        return self._match_type(message) and self._match_source(message) and self._match_target(message)

    def _match_type(self, message):
        return self._type_regex.match(message.type)

    def _match_source(self, message):
        return self._source_regex.match(message.source)

    def _match_target(self, message):
        return message.target is None or self._target_regex.match(message.target)

    def __call__(self, *args, **kwargs):
        return self.match(args[0])


class AllMessageFilter(MessageFilter):
    """
    MessageFilter that lets all messages through
    """

    def match(self, message):
        return True
