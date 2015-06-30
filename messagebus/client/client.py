import requests
import logging
import argparse
import json

from messagebus import Event
from messagebus.util import date_time_utils


DEFAULT_URL = "http://127.0.0.1:8007/post_message"

class MessageBusClient:

    def __init__(self, url):
        self.url = url

    def send_message(self, message):

        message_json = message.to_json()
        logging.debug("POST message to: %s", self.url)
        logging.debug("Send message: %s", message_json)

        headers = {'Content-type': 'application/json'}
        response = requests.post(self.url, data=message_json, headers=headers)

        logging.debug("Response status code %s", response.status_code)
        if response.status_code > 200:
            logging.debug(response.text)

        data = response.json()
        return data["message_id"]

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Read sensor readings and pass them to the messagebus.')
    parser.add_argument('-u', '--url', action="store", default=DEFAULT_URL, help='Messagebus URL')
    parser.add_argument("-t", "--type", action="store", required=True, help="Message type")
    parser.add_argument("-s", "--source", action="store", required=True, help="Message source")
    parser.add_argument("-d", "--data", action="store", default="{}", help="Message Data (JSON)")

    args = parser.parse_args()
    logging.debug(args)

    client = MessageBusClient(args.url)

    payload = json.loads(args.data)

    event = Event(source=args.source, type=args.type, data=payload, timestamp=date_time_utils.timestamp())

    id = client.send_message(event)

    logging.debug("Sent event {}".format(id))

