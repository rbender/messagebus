
import argparse
import logging
import serial

from messagebus.client import MessageBusClient
from messagebus.util.simple_sensor_parser import SimpleSensorParser

DEFAULT_PORT = "/dev/tty.usbmodem1411"
DEFAULT_BAUD = 9600
DEFAULT_URL = "http://127.0.0.1:8007/post_message"

class SimpleSensorPublisherProcess():

    def __init__(self, connection, url):
        self.logger = logging.getLogger("SimpleSensorPublisherProcess")
        self.connection = connection
        self.client = MessageBusClient(url)
        self.parser = SimpleSensorParser()

    def start(self):
        while True:
            line = connection.readline()
            events = self.parser.parse(line)
            for event in events:
                self.client.send_message(event)

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s %(asctime)s %(filename)s:%(lineno)d: %(message)s')

    parser = argparse.ArgumentParser(description='Read sensor readings and pass them to the messagebus.')
    parser.add_argument('-p', '--port', action="store", default=DEFAULT_PORT, help='Serial port')
    parser.add_argument('-b', '--baud', action="store", default=DEFAULT_BAUD, type=int, help='Baud rate')
    parser.add_argument('-u', '--url', action="store", default=DEFAULT_URL, help='Messagebus URL')

    args = parser.parse_args()
    logging.debug(args)

    connection = serial.Serial(args.port, args.baud)
    publisher = SimpleSensorPublisherProcess(connection, args.url)
    publisher.start()
