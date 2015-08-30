from Adafruit_IO import Client

import logging

from messagebus import MessageHandler

class AdafruitHandler(MessageHandler):

    def __init__(self, api_key, feed, message_field = "value"):
        self.message_field = message_field
        self.client = Client(api_key)
        self.feed = feed

    def send_value(self, value):

        logging.debug("Send value %s to feed %s", value, self.feed)
        self.client.send(self.feed, value)

    def handle(self, message):

        value = message.data[self.message_field]
        self.send_value(value)


if __name__ == "__main__":

    adafruit = AdafruitHandler("<YOUR-KEY-HERE>", "<FEED>")

    adafruit.send_value(78)
