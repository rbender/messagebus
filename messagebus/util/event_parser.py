import json

from messagebus import Message
from messagebus.util import date_time_utils

def build_message_from_form_data(form):

    now = date_time_utils.timestamp()

    #Required fields
    category = form['category']
    source = form['source']
    type = form['type']

    #Optional fields
    target = form.get('target')
    timestamp = form.get('timestamp', now)

    data = json.loads(form.get('data', default="{}"))

    return Message(category=category, source=source, type=type, target=target, data=data, timestamp=timestamp, received_timestamp=now)

def build_message_from_json(message_json):

    now = date_time_utils.timestamp()

    #Required fields
    category = message_json['category']
    source = message_json['source']
    type = message_json['type']

    #Optional fields
    target = message_json.get('target')
    timestamp = message_json.get('timestamp', now)

    data = message_json.get('data', {})

    return Message(category=category, source=source, type=type, target=target, data=data, timestamp=timestamp, received_timestamp=now)
