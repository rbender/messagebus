from messagebus import MessageHandler

ONE_HOUR = 60 * 60 * 1000

class HeartbeatHandler(MessageHandler):
    """
    Keeps track of the timestamp of the last message received for a device. This can later be
    used to keep track of which devices haven't been heard from in awhile and to send alerts
    when they haven't been heard from in a certain amount of time.

    Currently this handler needs to hear from a device at least once to even begin tracking
    time.

    TODO:
    - Start a thread to send alerts when a device hasn't been heard from since the timeout
    - Persist data so it survives a reboot
    - Get list of devices from registry
    - Support custom per-device timeouts (via registry or dedicated heartbeat message?)

    """

    def __init__(self, default_timeout_minutes = 60):
        self.timeout = default_timeout_minutes
        self.last_heartbeast_times = {} # Map device_id -> timestamp

    def handle(self, message):

        device_id = message.source

        self.last_heartbeast_times[device_id] = message.received_timestamp
