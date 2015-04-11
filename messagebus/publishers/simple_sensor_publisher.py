
import logging
import serial
import threading
import time
import json

from messagebus import Event
from messagebus.util import SerialBuffer

class SimpleSensorPublisher(threading.Thread):

    def __init__(self, connection, context):
        self.logger = logging.getLogger("SimpleSensorPublisher")
        self.connection = connection
        self.context = context
        self.messagebus = context["messagebus"]
        self.running = False
        self.buffer = SerialBuffer(connection)
        threading.Thread.__init__(self)


    def run(self):
        self.logger.info("Starting")
        self.running = True
        self.monitor_serial()

    def monitor_serial(self):
        while self.running:
            line = self.buffer.readline()
            if line is not None:
                self.process_line(line)
        self.connection.close()
        self.logger.info("Stopped")

    def process_line(self, line):
        self.logger.debug(line)
        message = self.parse_line(line)
        if message is not None:
            self.process_message(message)

    def process_message(self, message):
        self.logger.debug(message)
        for sensor in message["sensors"]:
            self.process_sensor_reading(sensor)

    def process_sensor_reading(self, sensor):
        name = sensor["name"]
        value = sensor["raw_value"]
        self.logger.debug("{} = {}".format(name, value))

        source = "arduino." + name
        data = {"value" : value}
        event = Event(source=source, type="reading", data=data)

        if self.messagebus is not None:
            self.messagebus.send_message(event)

    def parse_line(self, line):
        try:
            message = json.loads(line)
            return message
        except ValueError as ex:
            print ex
            return None

    def stop(self):
        self.running = False
        self.logger.info("Stopping")

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    connection = serial.Serial("/dev/tty.usbmodem1411", 9600, timeout=0)
    publisher = SimpleSensorPublisher(connection, {"messagebus":None})
    publisher.start()
    time.sleep(20)
    publisher.stop()
    print "Stopping"
