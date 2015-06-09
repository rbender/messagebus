from messagebus import MessageListener
import messagebus.util.pattern_matching as pattern_matcher
import xively

class XivelyListener(MessageListener):
    """
    MessageListener that posts messages to Xively.

    The Xively info (feed, api key, etc) is configured on a device-by-device
    basis through the DeviceMetadataService.
    """

    def __init__(self, device_metadata_service):
        self.device_metadata_service = device_metadata_service

    def handle(self, message):

        xively_config = self.lookup_config(message.source, message.type)
        datastream = self.get_datastream(xively_config)

        # Allow configuration of which event data field to post. Default is "value"
        field_name = xively_config.get("field", "value")
        datastream.datapoints.create(value=message.data[field_name])

    def lookup_config(self, source, type):
        config = self.device_metadata_service.get_device(source)["xively"]

        if config.has_key("feed"):
            return config

        # If a device can emit multiple types of events, then we can
        # specify different configurations for each event type.
        # This supports wildcard matching for event types.
        for type_pattern in config.keys():
            if pattern_matcher.match_pattern(type, type_pattern):
                return config[type_pattern]

    def get_datastream(self, xively_config):
        feed_id = xively_config["feed"]
        api_key = xively_config["key"]
        datastream = xively_config["datastream"]

        client = xively.XivelyAPIClient(api_key)
        feed = client.feeds.get(feed_id)
        return feed.datastreams.get(datastream)

