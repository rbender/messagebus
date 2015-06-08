import glob
import json
import logging
import os.path

class DeviceRegistry:
    """
    Service for looking up information about a device, such as its physical location. Can also
    be used to store device-specific configuration for a service, such as Xively.

    Devices are identified by a string which should correspond to the "source" attribute
    of a message. Device metadata is simply a dict object.

    Devices can be added manually or loaded from JSON files in a configuration directory.
    """

    def __init__(self):
        self._devices = {}
        self.logger = logging.getLogger("DeviceRegistry")

    def add_device(self, device_id, metadata):

        self.logger.debug("Add device %s : %s", device_id, metadata)

        self._devices[device_id] = metadata

    def get_device(self, device_id):
        return self._devices[device_id]

    def remove_device(self, device_id):

        self.logger.debug("Remove device %s", device_id)

        del self._devices[device_id]

    def list_devices(self):
        return self._devices.keys()

    def load_from_path(self, path):
        self.logger.debug("Load device config from %s", path)

        for filename in glob.glob(path + "/*.json"):
            id, metadata = self._load_file(filename)
            self.add_device(id, metadata)

    def _load_file(self, filename):
        self.logger.debug("Load device metadata %s", filename)

        name = os.path.split(filename)[1]
        device_id = os.path.splitext(name)[0]
        self.logger.debug("Found device %s", device_id)

        file = open(filename)
        metadata = json.load(file)

        return device_id, metadata
