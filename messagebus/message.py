import json

from util import ToStringBuilder
from util import date_time_utils

class Message:
    """
    Simple message class. Can represent a reading, command, etc
    """

    def __init__(self, **kwargs):
        self.category = kwargs.get("category")
        self.id = kwargs.get("id", 0)
        self.type = kwargs.get("type")
        self.source = kwargs.get("source")
        self.target = kwargs.get("target")
        self.timestamp = kwargs.get("timestamp", date_time_utils.timestamp())
        self.data = kwargs.get("data", {})

    def __str__(self):
        builder = ToStringBuilder("Message")
        builder.append("category", self.category)
        builder.append("id", self.id)
        builder.append("timestamp", self.timestamp)
        builder.append("type", self.type)
        builder.append("source", self.source)
        builder.append("target", self.target)
        builder.append("data", self.data)
        return builder.to_string()

    def to_json(self):
        return json.dumps(self.__dict__)

