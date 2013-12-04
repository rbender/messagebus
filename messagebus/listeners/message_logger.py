"""
MessageListener that logs messages to file. Each message message is
serialized to a JSON string and written on a single line.
"""
import logging

from messagebus import MessageListener

class MessageFileLogger(MessageListener):

    def __init__(self, filename):

        self.logger = logging.getLogger("MessageFileLogger")
        self.logger.info("Log messages to {}".format(filename))
        self.filename = filename

    def handle(self, message):

        json_string = message.to_json()
        self.logger.debug("Log: {}".format(json_string))
        self.write_to_file(self.filename, json_string)

    def write_to_file(self, filename, text):
        with open(self.filename, "a") as file:
            file.write(text)
            file.write("\n")