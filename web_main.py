import logging

from webapp import server

from messagebus import MessageBus

from messagebus.store import MemoryMessageStore
from messagebus.services import DeviceMetadataService
from messagebus.configuration.init_script_loader import load_init_scripts

logging.basicConfig(level=logging.DEBUG)

# Initialize the message store
message_store = MemoryMessageStore()
server.message_store = message_store

# Load and populate DeviceMetadataService from the config/devices
# directory. In the future, this path should be configurable
devices = DeviceMetadataService()
devices.load_from_path("config/devices")
server.devices = devices

# Initialize the message bus
message_bus = MessageBus()
server.messagebus = message_bus

# Create context object and call init scripts
context = {}
context["messagebus"] = message_bus
context["devices"] = devices
context["message_store"] = message_store

load_init_scripts("config/init_scripts", context)

server.app.run()