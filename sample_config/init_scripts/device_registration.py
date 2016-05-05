from messagebus.handlers.device_registration_handler import DeviceRegistrationHandler, DeviceDeregistrationHandler
from messagebus.messagefilter import PatternMessageFilter

def init(context):

    message_bus = context["messagebus"]
    device_registry = context["device_registry"]

    register_listener = DeviceRegistrationHandler(device_registry)
    register_filter = PatternMessageFilter(type="device.register")

    message_bus.subscribe(register_listener, register_filter)

    deregister_listener = DeviceDeregistrationHandler(device_registry)
    deregister_filter = PatternMessageFilter(type="device.deregister")

    message_bus.subscribe(deregister_listener, deregister_filter)