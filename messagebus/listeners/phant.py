from messagebus import MessageListener

import requests

class PhantListener(MessageListener):

    def __init__(self, url, private_key, param_name, message_field = "value"):
        self.url = url
        self.private_key = private_key
        self.param_name = param_name
        self.message_field = message_field

    def send_value(self, value):

        headers = {"Phant-Private-Key" : self.private_key, "Accept" : "application/json"}
        post_data = {self.param_name : value}

        requests.post(self.url, data=post_data, headers=headers)

    def handle(self, message):

        value = message.data[self.message_field]
        self.send_value(value)


if __name__ == "__main__":

    phant = PhantListener("https://data.sparkfun.com/input/o840W6LndVFxmZALVRKb", "yzegyJPw2GCemYWpPz25", "temperature")

    phant.send_value(78)