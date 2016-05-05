import requests
import logging
import argparse


from messagebus.client import MessageBusClient
from messagebus.client.client import DEFAULT_URL

class InternetCheckPublisher():

    def __init__(self, url_to_check, messagebus_url, interval):
        self.url_to_check = url_to_check
        self.client = MessageBusClient(messagebus_url)
        self.interval = interval


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Check internet connection')
    parser.add_argument('-w', '--website', action="store", help="URL to poll")
    parser.add_argument('-i', '--interval', action="store", help="Polling interval (seconds)")
    parser.add_argument('-u', '--url', action="store", default=DEFAULT_URL, help='Messagebus URL')

    args = parser.parse_args()
    logging.debug(args)

    publisher = InternetCheckPublisher(args.website, args.mess)
    publisher.start()

