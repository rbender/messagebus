from messagebus.services import DeviceMetadataService

import logging
import unittest

class TestEvent(unittest.TestCase):

    def setUp(self):

        logging.basicConfig(level=logging.DEBUG)

        self.devices = DeviceMetadataService()

    def test_load__from_path(self):
        self.devices.load_from_path("test_config/devices")

        device = self.devices.get_device("test_device")
        self.assertIsNotNone(device)
        self.assertEquals("bar", device["foo"])

