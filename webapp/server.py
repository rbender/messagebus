from flask import Flask
from flask import render_template, request, Response

from messagebus import Message
from messagebus.util.simple_sensor_parser import SimpleSensorParser
from messagebus.util import date_time_utils

from messagebus.configuration.init_script_loader import shutdown_scripts

import json
import time

app = Flask(__name__)
app.debug = True

#Initialize these outside of this module
messagebus = None
message_store = None
devices = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/message_form")
def message_form():
    return render_template("message_form.html")

@app.route("/post_message", methods=['POST'])
def post_message():

    if request.content_type == "application/x-www-form-urlencoded":
        message = build_message_from_form_data(request.form)
        messagebus.send_message(message)
        return "Posted Message {}".format(message.id)

    elif request.content_type == "application/json":
        message = build_message_from_json(request.get_json())
        messagebus.send_message(message)

        response_data = {"message_id" : message.id}
        response_json = json.dumps(response_data)

        return Response(response=response_json, status=200, mimetype="application/json")

    else:
        return Response(response="Unsupported Media Type", status=415)

@app.route("/post_simple_sensors", methods=['POST'])
def post_simple_sensors():

    sensors_json = request.get_json()
    parser = SimpleSensorParser()
    events = parser.convert_to_events(sensors_json)

    event_ids = []
    for event in events:
        event_id = messagebus.send_message(event)
        event_ids.append(event_id)

    return "Posted Messages: " + str(event_ids)

@app.route("/messages/<int:id>", methods=['GET'])
def get_message(id):

    message = message_store.load_message(id)
    return Response(response=message.to_json(indent=4),
                    status=200,
                    mimetype="application/json")

@app.route("/devices/", methods=['GET'])
def list_devices():

    device_ids = devices.list_devices()

    return render_template("devices.html", devices=device_ids)

@app.route("/devices/<id>", methods=['GET'])
def get_device(id):

    device = devices.get_device(id)
    return Response(response=json.dumps(device, indent=4),
                    status=200,
                    mimetype="application/json")

@app.route('/shutdown', methods=['POST','GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

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

def shutdown_server():
    shutdown_scripts()
    time.sleep(1)
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
