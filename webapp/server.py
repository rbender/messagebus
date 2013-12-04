from flask import Flask
from flask import render_template, request

from messagebus import Message, MessageBus, AllMessageFilter
from messagebus.listeners import MessageFileLogger

import json

app = Flask(__name__)
app.debug = True

messagebus = MessageBus()

message_file_logger = MessageFileLogger("messages.log")
message_filter = AllMessageFilter()

messagebus.subscribe(message_file_logger, message_filter)

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

    return "Message Posted"

