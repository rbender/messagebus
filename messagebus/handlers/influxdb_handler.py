from influxdb import InfluxDBClient
from messagebus import MessageHandler
from messagebus.util import message_utils
from messagebus import Message
from messagebus.util import log_utils
import logging


class InfluxDbReadingHandler(MessageHandler):

    def __init__(self, influx_client):
        self.client = influx_client
        self.logger = logging.getLogger("InfluxDbReadingHandler")

    def handle(self, message):

        reading_type = message_utils.get_reading_type(message)
        reading_value = message.data["value"] * 1.0

        influx_data = {
            "measurement": reading_type,
            "tags": {
                "device": message.source
            },
            "time": message.timestamp,
            "fields": {
                "value": reading_value
            }
        }

        self.logger.debug("Write data to InfluxDB: %s", influx_data)

        self.client.write_points([influx_data], time_precision='ms')

if __name__ == "__main__":

    log_utils.init()

    client = InfluxDBClient(database="home_automation")

    message = message_utils.build_message(source="foo.bar", type="event.device.sensor.reading.test", data={"value" : 123})

    handler = InfluxDbReadingHandler(client)
    handler.handle(message)

