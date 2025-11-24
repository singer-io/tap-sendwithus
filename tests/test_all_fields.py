from base import SendwithusBaseTest
from tap_tester.base_suite_tests.all_fields_test import AllFieldsTest


class SendwithusAllFields(AllFieldsTest, SendwithusBaseTest):
    """Ensure running the tap with all streams and fields selected results in
    the replication of all fields."""
    MISSING_FIELDS = {
        # These fields don't appear in the API response
        "log_events": [
            "type",
            "message"
        ]
    }

    @staticmethod
    def name():
        return "tap_tester_sendwithus_all_fields_test"

    def streams_to_test(self):
        streams_to_exclude = {}
        return self.expected_stream_names().difference(streams_to_exclude)
