import requests
import logging


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
