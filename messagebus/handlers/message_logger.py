"""
MessageListener that logs messages to file. Each message message is
serialized to a JSON string and written on a single line.
"""
import logging
import time

from messagebus import MessageHandler

class MessageFileLogger(MessageHandler):

    def __init__(self, filename_prefix, filename_extension=".log"):

        self.logger = logging.getLogger("MessageFileLogger")
        self.logger.info("Log messages to {}".format(filename_prefix))
        self.filename_prefix = filename_prefix
        self.filename_extension = filename_extension

    def handle(self, message):

        filename = self.build_filename()

        json_string = message.to_json()
        self.logger.debug("Log: {} to {}".format(json_string, filename))
        self.write_to_file(filename, json_string)

    def build_filename(self):

        now = time.gmtime()
        suffix = str(now.tm_year) + "-" + str(now.tm_mon) + "-" + str(now.tm_mday)
        return self.filename_prefix + suffix + self.filename_extension

    def write_to_file(self, filename, text):
        with open(filename, "a") as file:
            file.write(text)
            file.write("\n")
