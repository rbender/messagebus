import logging
import threading
import uuid

from messagesubscription import MessageSubscription
from util import date_time_utils

class MessageBus:

    def __init__(self):
        self.logger = logging.getLogger("MessageBus")
        self.subscriptions = []
        self.counter = date_time_utils.timestamp()
        self._thread_constructor = threading.Thread
        self.logger.debug("Message bus initialized")

    def subscribe(self, listener, message_filter):
        subscription = MessageSubscription(message_filter, listener)
        self.subscriptions.append(subscription)
        return subscription

    def unsubscribe(self, subscription):
        self.subscriptions.remove(subscription)

    def send_message(self, message):
        message.id = self.__generate_id()
        self.__notify_subscribers(message)
        return message.id

    def __notify_subscribers(self, message):
        self.logger.debug("Send message: {}".format(message))
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

