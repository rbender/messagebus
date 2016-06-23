import logging
import threading
import uuid
import json

import paho.mqtt.client as mqtt

from messagesubscription import MessageSubscription
from message import Message
from util import date_time_utils

class MessageBus:

    def __init__(self, mqtt_host, mqtt_port, mqtt_topic="messagebus"):
        self.logger = logging.getLogger(__name__)
        self.subscriptions = []
        self.counter = date_time_utils.timestamp()
        self._thread_constructor = threading.Thread
        self.logger.debug("Message bus initialized")

        self.mqtt_client = mqtt.Client(client_id="messagebus-backend", clean_session=False)
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic

        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_subscribe = self.on_subscribe

        self.connected = False

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info("Connected to MQTT: %s", rc)
        self.connected = True

        self.logger.info("Subscribe to topic %s", self.mqtt_topic)
        self.mqtt_client.subscribe(self.mqtt_topic, qos=1)

    def on_disconnect(self, client, userdata, rc):
        self.logger.warn("Disconnected from MQTT: %s", rc)
        self.connected = False

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.logger.info("Subscribed %s, %s", mid, granted_qos)

    def on_message(self, client, userdata, msg):

        message_body = msg.payload
        self.logger.debug("Received message %s", message_body)

        message = None
        try:
            message = self.parse_message(message_body)
        except Exception as ex:
            self.logger.error("Cannot parse message: %s", ex)

        if message is not None:
            self.__notify_subscribers(message)

    def parse_message(self, message_body):
        message_json = json.loads(message_body)

        now = date_time_utils.timestamp()

        #Required fields
        id = message_json["id"]
        source = message_json['source']
        type = message_json['type']

        #Optional fields
        target = message_json.get('target')
        timestamp = message_json.get('timestamp', now)
        received_timestamp = message_json.get('received_timestamp', now)

        data = message_json.get('data', {})

        return Message(id=id, source=source, type=type, target=target, data=data, timestamp=timestamp, received_timestamp=received_timestamp)

    def connect(self):
        self.logger.info("Connect to MQTT Server %s:%s", self.mqtt_host, self.mqtt_port)

        self.mqtt_client.connect(self.mqtt_host, port=self.mqtt_port)

        self.logger.info("Loop forever")
        self.mqtt_client.loop_forever()

    def subscribe(self, listener, message_filter):
        subscription = MessageSubscription(message_filter, listener)
        self.subscriptions.append(subscription)
        return subscription

    def unsubscribe(self, subscription):
        self.subscriptions.remove(subscription)

    def __notify_subscribers(self, message):
        self.logger.debug("Send message to subscribers: {}".format(message))
        for subscription in self.subscriptions:
            if subscription.match(message):
                self.__notify_subscriber(subscription, message)

    def __notify_subscriber(self, subscription, message):
        """
        Passes a message to a subscriber in a separate thread
        """

        self.logger.debug("Send message to {}".format(subscription))
        thread = self._thread_constructor(target=lambda: subscription.handle(message))
        thread.start()

    def __generate_id(self):
        return str(uuid.uuid1())

