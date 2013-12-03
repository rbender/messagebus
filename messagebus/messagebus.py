import logging
import threading

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
        self.__send_message_to_subscribers(message)

    def __send_message_to_subscribers(self, message):
        self.logger.debug("Send message: {}".format(message))
        for subscription in self.subscriptions:
            if subscription.match(message):
                self.__send_message_to_subscriber(subscription, message)

    def __send_message_to_subscriber(self, subscription, message):
        """
        Passes a message to a subscriber in a separate thread
        """

        thread = self._thread_constructor(target=lambda: subscription.handle(message))
        thread.start()

    def __generate_id(self):
        new_id = self.counter
        self.counter += 1
        return new_id

