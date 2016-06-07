import logging
import uuid

import paho.mqtt.client as mqtt

class MessageBusWriter:

    def __init__(self, mqtt_host, mqtt_port, mqtt_topic="messagebus"):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Message Bus Writer initialized")


        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect

        self.connected = False

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info("Connected to MQTT: %s", rc)
        self.connected = True

    def on_disconnect(self, client, userdata, rc):
        self.logger.warn("Disconnected from MQTT: %s", rc)
        self.connected = False

    def connect(self):
        self.logger.info("Connect to MQTT Server")

        self.mqtt_client.connect(self.mqtt_host, port=self.mqtt_port)

        self.mqtt_client.loop_start()

    def send_message(self, message):
        message.id = self.__generate_id()
        message_json = message.to_json()

        self.mqtt_client.publish(self.mqtt_topic, payload=message_json, qos=1)

        return message.id

    def shutdown(self):
        self.logger.info("Shutdown")
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        self.connected = False

    def __generate_id(self):
        return str(uuid.uuid1())

