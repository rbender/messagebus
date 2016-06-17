"""
A list of common message types. Not exhaustive, but a good starting point
"""

EVENT_HEARTBEAT = "event.device.heartbeat"
EVENT_READING = "event.device.sensor.reading"
EVENT_TEMPERATURE = EVENT_READING + ".temperature"
EVENT_TARGET_TEMPERATURE = EVENT_READING + ".temperature.target"
EVENT_HUMIDITY = EVENT_READING + ".humidity"
EVENT_ERROR = "event.system.error"
EVENT_DEVICE_MISSING = "event.system.device.missing"

COMMAND_SHUTDOWN = "command.system.shutdown"
COMMAND_PING = "command.device.ping"


