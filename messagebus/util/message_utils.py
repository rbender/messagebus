from messagebus import Message
import uuid

def generate_id():
    return str(uuid.uuid1())

def get_reading_type(message):
    return message.type[len("event.device.sensor.reading."):]

def get_reading_value(message):
    return message.data['value']

def build_message(**kwargs):

    message = Message(**kwargs)
    message.id = generate_id()
    return message