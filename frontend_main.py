import logging
import argparse
from webapp import server

from messagebus import MessageBusWriter

DEFAULT_PORT = 8007
DEFAULT_HOST = "127.0.0.1"
DEFAULT_MQTT_HOST = "localhost"
DEFAULT_MQTT_PORT = 1883
CONFIG_ROOT = "config"

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s %(asctime)s %(filename)s:%(lineno)d: %(message)s')

parser = argparse.ArgumentParser(description='Read sensor readings and pass them to the messagebus.')
parser.add_argument('-p', '--port', action="store", default=DEFAULT_PORT, type=int, help='HTTP port to run on')
parser.add_argument('--host', action="store", default=DEFAULT_HOST, help='Host/IP to run on')
parser.add_argument('--mqtt-host', action="store", default=DEFAULT_MQTT_HOST, help='MQTT host to connect to')
parser.add_argument('--mqtt-port', action="store", default=DEFAULT_MQTT_PORT, help='MQTT port to connect to')

args = parser.parse_args()
logging.debug(args)

# Initialize the message bus
message_bus = MessageBusWriter(args.mqtt_host, args.mqtt_port)
message_bus.connect()
server.messagebus = message_bus

# Start flash web application
server.app.run(port=args.port, host=args.host, use_reloader=False)
