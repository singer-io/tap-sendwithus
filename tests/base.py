import os

from tap_tester.base_suite_tests.base_case import BaseCase


class SendwithusBaseTest(BaseCase):
    """Setup expectations for test sub classes.

    Metadata describing streams. A bunch of shared methods that are used
    in tap-tester tests. Shared tap-specific methods (as needed).
    """
    start_date = "2019-01-01T00:00:00Z"
    PARENT_TAP_STREAM_ID = "parent-tap-stream-id"

    @staticmethod
    def tap_name():
        """The name of the tap."""
        return "tap-sendwithus"

    @staticmethod
    def get_type():
        """The name of the tap."""
        return "platform.sendwithus"

    @classmethod
    def expected_metadata(cls):
        """The expected streams and metadata about the streams."""
        return {
            "templates": {
                cls.PRIMARY_KEYS: {"id"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"created"},
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
                cls.PARENT_TAP_STREAM_ID: None
            },
            "logs": {
                cls.PRIMARY_KEYS: {"id"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"created"},
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
                cls.PARENT_TAP_STREAM_ID: None
            },
            "log_events": {
                cls.PRIMARY_KEYS: {"log_id", "status", "created"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"created"},
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
                cls.PARENT_TAP_STREAM_ID: "logs"
            },
            "snippets": {
                cls.PRIMARY_KEYS: {"id"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"modified"},
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
                cls.PARENT_TAP_STREAM_ID: None
            },
            "drip_campaigns": {
                cls.PRIMARY_KEYS: {"id"},
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
                cls.PARENT_TAP_STREAM_ID: None
            }
        }

    @staticmethod
    def get_credentials():
        """Authentication information for the test account."""
        credentials_dict = {}
        creds = {'api_key': 'TAP_SENDWITHUS_API_KEY'}

        for cred in creds:
            credentials_dict[cred] = os.getenv(creds[cred])

        return credentials_dict

    def get_properties(self, original: bool = True):
        """Configuration of properties required for the tap."""
        return_value = {
            "start_date": self.start_date,
        }

        return return_value

    def expected_parent_tap_stream(self, stream=None):
        """return a dictionary with key of table name and value of parent stream"""
        parent_stream = {
            table: properties.get(self.PARENT_TAP_STREAM_ID, None)
            for table, properties in self.expected_metadata().items()}
        if not stream:
            return parent_stream
        return parent_stream[stream]
