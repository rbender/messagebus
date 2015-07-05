from messagebus import MessageHandler

import requests

class IfThisThenThatHandler(MessageHandler):

    def __init__(self, event_name, api_key, message_field = "value"):
        self.url = "https://maker.ifttt.com/trigger/%s/with/key/%s" % (event_name, api_key)
        self.message_field = message_field

    def send_value(self, value):

        json_data = {"value1" : value}

        return requests.post(self.url, json=json_data)

    def handle(self, message):

        value = message.data[self.message_field]
        return self.send_value(value)

if __name__ == "__main__":

    handler = IfThisThenThatHandler("some-event", "YOUR-KEY-HERE")

    print handler.send_value(78)