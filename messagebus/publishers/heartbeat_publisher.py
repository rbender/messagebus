from messagebus.client import MessageBusClient
from messagebus import Message

import messagebus.defaults as defaults
import messagebus.message_types as message_types
import messagebus.util.log_utils as log_utils

import time

HEARTBEAT_INTERVAL = 60

def send_heartbeat(device_id, client):

    message = Message(device_id = device_id, type=message_types.EVENT_HEARTBEAT)
    client.send_message(message)

if __name__ == "__main__":

    log_utils.init()

    #TODO Make configurable from command line
    client = MessageBusClient(url=defaults.DEFAULT_POST_MESSAGE_URL)

    while(True):

        send_heartbeat("test_device", client)

        time.sleep(HEARTBEAT_INTERVAL)