import messagebus.message_types as message_types
import messagebus.defaults as defaults

from messagebus.client import MessageBusClient

import time
import math

if __name__ == "__main__":

    bus_url = defaults.DEFAULT_POST_MESSAGE_URL
    messagebus_client = MessageBusClient(bus_url)

    while True:

        localtime = time.localtime()
        seconds_into_hour = localtime.tm_min * 60 + localtime.tm_sec        
        percent_into_hour = seconds_into_hour / 3600.0

        radians = percent_into_hour * 2 * math.pi

        value = math.sin(radians) * 100.0

        print value

        messagebus_client.send_reading("generator.sine", message_types.EVENT_TEMPERATURE, value=value, units="f")

        time.sleep(10)