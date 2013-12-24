import logging
import re

def expand_regex(pattern):

    regex = pattern
    regex = regex.replace(".", "\\.")
    regex = regex.replace("*", "(.*?)")

    logging.debug("Expand {pattern} to {regex}".format(pattern=pattern, regex=regex))

    return re.compile(regex)

def match_pattern(value, pattern):

    regex = expand_regex(pattern)
    return regex.match(value)
