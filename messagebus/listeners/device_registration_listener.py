"""
Listener that saves device deregistration to the device registry.
"""
from messagebus import MessageListener

class DeviceRegistrationListener(MessageListener):

    def __init__(self, device_registry):
        self.device_registry = device_registry

    def handle(self, message):

        device_id = message.data["device_id"]
        device_info = message.data["device_info"]

        #TODO Add persistent registrations

        self.device_registry.add_device(device_id, device_info)

class DeviceDeregistrationListener(MessageListener):

    def __init__(self, device_registry):
        self.device_registry = device_registry

    def handle(self, message):

        device_id = message.data["device_id"]

        self.device_registry.remove_device(device_id)