
import socket
import time

from messagebus import MessageHandler
import messagebus.util.message_utils as message_utils

class GraphiteHandler(MessageHandler):

    def __init__(self, server="localhost", port=2003, message_field="value"):
        self.server = server
        self.port = port
        self.message_field = message_field

    def send_value(self, path, value, timestamp):

        timestamp_seconds = timestamp / 1000

        message = '%s %s %d\n' % (path, value, timestamp_seconds)
        print message

        sock = socket.socket(socket.AF_INET)
        sock.connect((self.server, self.port))
        sock.sendall(message)
        sock.close()

    def handle(self, message):

        device_id = message.source
        sensor_id = message.data.get('sensor_id', None)
        reading_type = message_utils.get_reading_type(message)

        if sensor_id is not None:
            path = device_id + "." + sensor_id
        else:
            path = device_id + "." + reading_type

        value = message.data[self.message_field]
        timestamp = message.timestamp

        self.send_value(path, value, timestamp)


if __name__ == "__main__":

    handler = GraphiteHandler("127.0.0.1", 2003)

    message = message_utils.build_message(source="foo.baz.bat", type="event.device.sensor.reading.test", data={"value" : 70})

    handler.handle(message)

    #handler.send_value("foo.bar", 78, int(time.time() * 1000))

