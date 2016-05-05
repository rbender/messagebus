import nest
import nest.utils

import logging
import argparse
import time

from messagebus.client import MessageBusClient

DEFAULT_URL = "http://127.0.0.1:8007/post_message"
DEFAULT_INTERVAL = 60

class NestPublisher():

    def __init__(self, username, password, serial, device_id, bus_url, interval=DEFAULT_INTERVAL):
        self.client = nest.Nest(username, password)
        self.serial = serial
        self.device_id = device_id
        self.messagebus_client = MessageBusClient(bus_url)
        self.interval = interval
        self.logger = logging.getLogger("NestPublisher")

    def dump_device_data(self):

        for device in self.client.devices:
            logging.info("Device Name %s - Serial %s", device.name, device.serial)


    def get_device(self):

        for device in self.client.devices:
            if device._serial == self.serial:
                return device

        return None

    def poll_device(self):

        try:
            thermostat = self.get_device()
        except Exception as ex:
            self.logger.warn("Error getting thermostat: %s", ex)
            return

        if thermostat is None:
            raise Exception("Cannot find thermostat " + self.name)

        temperature_c = thermostat.temperature
        temperature_f = nest.utils.c_to_f(temperature_c)
        target_temperature_c = thermostat.target
        target_temperature_f = nest.utils.c_to_f(target_temperature_c)
        humidity = thermostat.humidity

        logging.debug("Temperature: %s", temperature_f)
        logging.debug("Target Temperature: %s", target_temperature_f)
        logging.debug("Humidity: %s", humidity)

        self.messagebus_client.send_event(self.device_id, "sensor.reading.temperature", value=temperature_f, units="f")
        self.messagebus_client.send_event(self.device_id, "sensor.reading.target_temperature", value=target_temperature_f, units="f")
        self.messagebus_client.send_event(self.device_id, "sensor.reading.humidity", value=humidity)

    def start(self):

        while True:
            self.poll_device()
            time.sleep(self.interval)

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s %(asctime)s %(filename)s:%(lineno)d: %(message)s')

    parser = argparse.ArgumentParser(description='Send Nest thermostat data to the messagebus.')
    parser.add_argument('-u', '--user', required=True, action="store", help='Nest username')
    parser.add_argument('-p', '--password', required=True, action="store", help='Nest password')
    parser.add_argument('-s', '--serial', required=True, action="store", help='Nest Serial Number')
    parser.add_argument('-d', '--device_id', required=True, action="store", help='Messagebus device id')
    parser.add_argument('-i', '--interval', action="store", help="Polling interval (seconds)")
    parser.add_argument('--url', action="store", default=DEFAULT_URL, help='Messagebus URL')

    args = parser.parse_args()
    logging.debug(args)

    publisher = NestPublisher(args.user, args.password, args.serial, args.device_id, args.url)
    publisher.start()
