from messagebus import MessageHandler

import requests

"""
IFTTT Handler supports posting data to the IFTTT service. The handler
is configured with the name of the custom event to post, your private
API KEY and the optional name of which message data field to post to the
value1 field.

I considered creating a full bridge to post *every* message the bus
receieves to IFTTT, but that could swamp the service. Also, we
would still need a way to convert each event's data to the simple
(value1,value2,value3) triple expected by IFTTT.

TODO: Add more flexible support for specifying which message fields go into
which value, possible using JsonPath expressions?

"""
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