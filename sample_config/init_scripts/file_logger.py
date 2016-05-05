from messagebus import AllMessageFilter
from messagebus.handlers import MessageFileLogger

import os.path
import logging

def init(context):

    logger = logging.getLogger("InitScriptLoader")

    log_path = os.path.expanduser("~/Library/Logs/messages.log")
    message_file_logger = MessageFileLogger(log_path)
    all_message_filter = AllMessageFilter()

    messagebus = context["messagebus"]
    messagebus.subscribe(message_file_logger, all_message_filter)
    logger.info("Registered file logger")
