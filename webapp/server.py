from flask import Flask
from flask import render_template, request, Response

from messagebus.util.simple_sensor_parser import SimpleSensorParser
import server_helper

import logging

import json

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
        message = server_helper.build_message_from_form_data(request.form)
        messagebus.send_message(message)
        return "Posted Message {}".format(message.id)

    elif request.content_type == "application/json":
        message = server_helper.build_message_from_json(request.get_json())
        messagebus.send_message(message)

        response_data = {"message_id" : message.id}
        response_json = json.dumps(response_data)

        return Response(response=response_json, status=200, mimetype="application/json")

    else:
        return Response(response="Unsupported Media Type", status=415)

@app.route("/heartbeat_form")
def heartbeat_form():
    return render_template("heartbeat_form.html")

@app.route("/post_heartbeat", methods=['POST'])
def post_heartbeat():

    message = server_helper.build_heartbeat_from_form_data(request.form)
    messagebus.send_message(message)
    return "Posted Message {}".format(message.id)

@app.route("/post_simple_sensors", methods=['POST'])
def post_simple_sensors():

    sensors_json = request.get_json(force=True)
    logging.debug(sensors_json)
    parser = SimpleSensorParser()
    events = parser.convert_to_events(sensors_json)

    event_ids = []
    for event in events:
        event_id = messagebus.send_message(event)
        event_ids.append(event_id)

    return "Posted Messages: " + str(event_ids)

@app.route('/shutdown', methods=['POST','GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def shutdown_server():

    messagebus.shutdown()

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
