import messagebus.message_types as message_types
import messagebus.defaults as defaults

from messagebus.client import MessageBusClient

import time
import math
import random

if __name__ == "__main__":

    bus_url = defaults.DEFAULT_POST_MESSAGE_URL
    messagebus_client = MessageBusClient(bus_url)
    
    value = 0

    while True:

        adjustment = random.randrange(-10,10) / 10.0
        value = value + adjustment

        print value

        messagebus_client.send_reading("generator.random", message_types.EVENT_TEMPERATURE, value=value, units="f")

        time.sleep(10)