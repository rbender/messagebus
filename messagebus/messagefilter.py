import logging
import re

class MessageFilter:

    def match(self, message):
        return False

class PatternMessageFilter(MessageFilter):

    def __init__(self, type, source):
        self.type = type
        self.source = source
        self._type_regex = expand_regex(type)
        self._source_regex = expand_regex(source)

    def match(self, message):
        return self._type_regex.match(message.type) and self._source_regex.match(message.source)

class AllMessageFilter(MessageFilter):
    """
    MessageFilter that lets all messages through
    """

    def match(self, message):
        return True

def expand_regex(pattern):

    regex = pattern
    regex = regex.replace(".", "\\.")
    regex = regex.replace("*", "(.*?)")

    logging.debug("Expand {pattern} to {regex}".format(pattern=pattern, regex=regex))

    return re.compile(regex)
