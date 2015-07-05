from messagebus import MessageHandler

import requests

class ThingSpeakHandler(MessageHandler):

    def __init__(self, url, api_key, param_name, message_field = "value"):
        self.url = url
        self.api_key = api_key
        self.param_name = param_name
        self.message_field = message_field

    def send_value(self, value):

        post_data = {"api_key" : self.api_key, self.param_name : value}

        return requests.post(self.url, params=post_data)

    def handle(self, message):

        value = message.data[self.message_field]
        return self.send_value(value)


if __name__ == "__main__":

    thingspeak = ThingSpeakHandler("https://api.thingspeak.com/update", "KANSU7TOPS6RWBQ6", "field1")

    print thingspeak.send_value(78)