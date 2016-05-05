
import socket
import time

from messagebus import MessageHandler

class GraphiteHandler(MessageHandler):

    def __init__(self, server, port, path, message_field = "value"):
        self.server = server
        self.port = port
        self.path = path
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

        value = message.data[self.message_field]
        timestamp = message.timestamp
        self.send_value(self.path, value, timestamp)


if __name__ == "__main__":

    handler = GraphiteHandler("rgb-ubuntu-vm.local", 2003, "foo.bar")

    handler.send_value("foo.bar", 78, int(time.time() * 1000))

