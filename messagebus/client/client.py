import requests
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter

import logging
import argparse
import json
import time

from messagebus import Message
from messagebus.util import date_time_utils


DEFAULT_URL = "http://127.0.0.1:8007/post_message"

class MessageBusClient:

    def __init__(self, url, max_retries=5, backoff_factor=1):
        self.url = url
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def send_message(self, message):

        message_json = message.to_json()
        logging.debug("POST message to: %s", self.url)
        logging.debug("Send message: %s", message_json)

        headers = {'Content-type': 'application/json'}

        session = requests.Session()

        if self.max_retries > 0:
            retry = Retry(total=self.max_retries, backoff_factor=self.backoff_factor)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)

        response = session.post(self.url, data=message_json, headers=headers)

        logging.debug("Response status code %s", response.status_code)
        if response.status_code > 200:
            logging.debug(response.text)

        data = response.json()
        return data["message_id"]

    def send(self, **data):

        message = Message(**data)
        self.send_message(message)

    def send_reading(self, source, type, value, units=None):

        data = {"value": value}
        if units is not None:
            data["units"] = units

        message = Message(source=source, type=type, data=data)
        self.send_message(message)

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Read sensor readings and pass them to the messagebus.')
    parser.add_argument('-u', '--url', action="store", default=DEFAULT_URL, help='Messagebus URL')
    parser.add_argument("-t", "--type", action="store", required=True, help="Message type")
    parser.add_argument("-s", "--source", action="store", required=True, help="Message source")
    parser.add_argument("-d", "--data", action="store", default="{}", help="Message Data (JSON)")
    parser.add_argument("-r", "--retries", action="store", default=5, type=int, help="Number of Retries")


    args = parser.parse_args()
    logging.debug(args)

    client = MessageBusClient(args.url, max_retries=args.retries)

    payload = json.loads(args.data)

    message = Message(source=args.source, type=args.type, data=payload, timestamp=date_time_utils.timestamp())

    start_time = time.time()

    try:
        id = client.send_message(message)
        logging.debug("Sent event {}".format(id))

    finally:

        duration = time.time() - start_time
        logging.debug("Duration: %s seconds", duration)



