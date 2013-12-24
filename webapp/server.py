from flask import Flask
from flask import render_template, request, Response

from messagebus import Message

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

    #TODO Validate these fields
    category = request.form['category']
    source = request.form['source']
    type = request.form['type']
    target = request.form['target']
    data = json.loads(request.form['data'])

    message = Message(category=category, source=source, type=type, target=target, data=data)
    messagebus.send_message(message)

    return "Posted Message {}".format(message.id)

@app.route("/message/<int:id>", methods=['GET'])
def get_message(id):

    message = message_store.load_message(id)
    return message.to_json()

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

