import logging
import json
import date_time_utils

from messagebus import Message
import messagebus.message_types as message_types

class SimpleSensorParser:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parse(self, line):

        self.logger.debug(line)
        message = self.parse_json(line)
        if message is not None:
            return self.convert_to_events(message)
        else:
            return []


    def convert_to_events(self, message):
        self.logger.debug(message)
        device_id = message["id"]

        events = []
        for sensor in message["sensors"]:
            event = self.convert_reading_to_event(device_id, sensor)
            events.append(event)
        return events

    def convert_reading_to_event(self, device_id, sensor):
        sensor_id = sensor["id"]
        value = sensor["value"]
        self.logger.debug("{} = {}".format(sensor_id, value))

        event_type = message_types.EVENT_READING + "." + sensor["type"]

        data = {"value" : value, "sensor_id" : sensor_id}

        if sensor.has_key("units"):
            data["units"] = sensor["units"]

        return Message(source=device_id, type=event_type, data=data, timestamp=date_time_utils.timestamp())

    def parse_json(self, line):
        try:
            message = json.loads(line)
            return message
        except ValueError as ex:
            print ex
            return None
