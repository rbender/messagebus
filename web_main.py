import logging

from webapp import server

from messagebus import MessageBus, AllMessageFilter, PatternMessageFilter
from messagebus.listeners import MessageFileLogger, MessageStoreListener, XivelyListener
from messagebus.store import MemoryMessageStore
from messagebus.services import DeviceMetadataService

logging.basicConfig(level=logging.DEBUG)

message_file_logger = MessageFileLogger("messages.log")
all_message_filter = AllMessageFilter()

message_store = MemoryMessageStore()
message_store_listener = MessageStoreListener(message_store)
server.message_store = message_store

devices = DeviceMetadataService()
devices.load_from_path("config/devices")
server.devices = devices

#xively_listener = XivelyListener(devices)
#xively_filter = PatternMessageFilter("reading", "*")

message_bus = MessageBus()
server.messagebus = message_bus

server.messagebus.subscribe(message_file_logger, all_message_filter)
server.messagebus.subscribe(message_store_listener, all_message_filter)
#server.messagebus.subscribe(xively_listener, xively_filter)

server.app.run()