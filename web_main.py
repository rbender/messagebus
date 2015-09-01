import logging
import argparse
from webapp import server

from messagebus import MessageBus
from messagebus.services.store import MemoryMessageStore
from messagebus.services import DeviceRegistry
from messagebus.configuration.init_script_loader import load_init_scripts, shutdown_scripts

DEFAULT_PORT = 8007
DEFAULT_HOST = "127.0.0.1"
CONFIG_ROOT = "config"

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='Read sensor readings and pass them to the messagebus.')
parser.add_argument('-p', '--port', action="store", default=DEFAULT_PORT, type=int, help='HTTP port to run on')
parser.add_argument('--host', action="store", default=DEFAULT_HOST, help='Host/IP to run on')
parser.add_argument('-c', '--config', action="store", default=CONFIG_ROOT, help='Path to configuration')

args = parser.parse_args()
logging.debug(args)

# Initialize the message store
message_store = MemoryMessageStore()
server.message_store = message_store

# Load and populate DeviceMetadataService from the config/devices
# directory. In the future, this path should be configurable
devices = DeviceRegistry()
devices.load_from_path(args.config + "/devices")
server.devices = devices

# Initialize the message bus
message_bus = MessageBus()
server.messagebus = message_bus

# Create context object and call init scripts
context = {}
context["messagebus"] = message_bus
context["device_registry"] = devices
context["message_store"] = message_store

load_init_scripts(args.config + "/init_scripts", context)

# Start flash web application
server.app.run(port=args.port, host=args.host, use_reloader=False)
