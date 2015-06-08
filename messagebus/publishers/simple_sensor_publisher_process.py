
import logging
import serial

from messagebus.client import MessageBusClient
from messagebus.util.simple_sensor_parser import SimpleSensorParser

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

    logging.basicConfig(level=logging.DEBUG)

    connection = serial.Serial("/dev/tty.usbmodem1411", 9600)
    publisher = SimpleSensorPublisherProcess(connection, "http://127.0.0.1:8000/post_message")
    publisher.start()
