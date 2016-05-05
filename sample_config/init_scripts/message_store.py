from messagebus.handlers import MessageStoreHandler
from messagebus import AllMessageFilter

import logging

def init(context):

    message_store = context["message_store"]
    messagebus = context["messagebus"]

    message_store_listener = MessageStoreHandler(message_store)
    all_message_filter = AllMessageFilter()

    messagebus.subscribe(message_store_listener, all_message_filter)
