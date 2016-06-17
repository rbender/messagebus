"""
Simple module for getting the current unix timestamp in milliseconds.
Includes methods to mocking out the current time for use in unit tests.
Inspired by the Java JodaTime DateTimeUtils class
"""

from time import time
from datetime import datetime

__use_fixed_timestamp = False
__fixed_timestamp = -1

def timestamp():
    """
    Get the current system time in milliseconds since epoch
    """
    global __use_fixed_timestamp
    if __use_fixed_timestamp:
        return __fixed_timestamp
    else:
        #TODO Make sure this is UTC
        return int(time() * 1000)

def unix_timestamp_to_datetime(timestamp):

    return datetime.utcfromtimestamp(timestamp / 1000)

def set_fixed_timestamp(timestamp):
    """
    Use a fixed a timestamp for the timestamp() method. This should only be used
    for unit testing
    """
    global __use_fixed_timestamp, __fixed_timestamp
    __use_fixed_timestamp = True
    __fixed_timestamp = timestamp

def set_use_system_timestamp():
    """
    Use the system time for the timestamp() method. This is only needed
    after using the set_fixed_timestamp() method, such as in the tearDown
    method of a unit test
    """
    global __use_fixed_timestamp
    __use_fixed_timestamp = False
