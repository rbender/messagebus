
from messagebus import Message
from messagebus.util import date_time_utils

import messagebus.message_types as message_types

import logging
import json

def build_message_from_form_data(form):

    now = date_time_utils.timestamp()

    #Required fields
    source = form['source']
    type = form['type']

    #Optional fields
    target = form.get('target')
    timestamp = form.get('timestamp', now)

    data = json.loads(form.get('data', default="{}"))

    return Message(source=source, type=type, target=target, data=data, timestamp=timestamp, received_timestamp=now)

def build_heartbeat_from_form_data(form):

    now = date_time_utils.timestamp()

    #Required fields
    source = form['source']
    type = message_types.EVENT_HEARTBEAT

    data = {}

    return Message(source=source, type=type, data=data, received_timestamp=now)

def build_message_from_json(message_json):

    now = date_time_utils.timestamp()

    #Required fields
    source = message_json['source']
    type = message_json['type']

    #Optional fields
    target = message_json.get('target')
    timestamp = message_json.get('timestamp', now)

    data = message_json.get('data', {})

    return Message(source=source, type=type, target=target, data=data, timestamp=timestamp, received_timestamp=now)

