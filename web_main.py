import logging

from webapp import server

from messagebus import Message, MessageBus, AllMessageFilter
from messagebus.listeners import MessageFileLogger, MessageStoreListener
from messagebus.store import MemoryMessageStore

logging.basicConfig(level=logging.DEBUG)

message_file_logger = MessageFileLogger("messages.log")
all_message_filter = AllMessageFilter()

message_store = MemoryMessageStore()
message_store_listener = MessageStoreListener(message_store)
server.message_store = message_store

server.messagebus.subscribe(message_file_logger, all_message_filter)
server.messagebus.subscribe(message_store_listener, all_message_filter)

server.app.run()