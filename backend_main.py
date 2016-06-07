import logging
import argparse

from messagebus import MessageBus
from messagebus.services.store import MemoryMessageStore
from messagebus.services import DeviceRegistry
from messagebus.configuration.init_script_loader import load_init_scripts, shutdown_scripts

DEFAULT_MQTT_HOST = "localhost"
DEFAULT_MQTT_PORT = 1883
CONFIG_ROOT = "config"

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s %(asctime)s %(filename)s:%(lineno)d: %(message)s')

parser = argparse.ArgumentParser(description='Read sensor readings and pass them to the messagebus.')
parser.add_argument('--mqtt-host', action="store", default=DEFAULT_MQTT_HOST, help='MQTT host to connect to')
parser.add_argument('--mqtt-port', action="store", default=DEFAULT_MQTT_PORT, help='MQTT port to connect to')
parser.add_argument('-c', '--config', action="store", default=CONFIG_ROOT, help='Path to configuration')

args = parser.parse_args()
logging.debug(args)

# Initialize the message store
message_store = MemoryMessageStore()

# Load and populate DeviceMetadataService from the config/devices
# directory. In the future, this path should be configurable
devices = DeviceRegistry()
devices.load_from_path(args.config + "/devices")

# Initialize the message bus
message_bus = MessageBus(args.mqtt_host, args.mqtt_port)

# Create context object and call init scripts
context = {}
context["messagebus"] = message_bus
context["device_registry"] = devices
context["message_store"] = message_store

load_init_scripts(args.config + "/init_scripts", context)

message_bus.connect()
