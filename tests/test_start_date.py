from base import SendwithusBaseTest
from tap_tester.base_suite_tests.start_date_test import StartDateTest


class SendwithusStartDateTest(StartDateTest, SendwithusBaseTest):
    """Instantiate start date according to the desired data set and run the
    test."""

    # Note: Start date test may fail for logs and log_events as the sendwithus Account has 7 day data retention policy(free version).
    # User may need to regenerate data within the retention period to have consistent test results using `generate-logs-data.py` present in spikes.
    # Also create new templates and snippets with created/modified date after start_date_2 to have data for both syncs.

    @staticmethod
    def name():
        return "tap_tester_sendwithus_start_date_test"

    def streams_to_test(self):
        streams_to_exclude = {"drip_campaigns"}  # Excluding drip_campaigns since it uses full table replication
        return self.expected_stream_names().difference(streams_to_exclude)

    @property
    def start_date_1(self):
        return "2015-03-25T00:00:00Z"

    @property
    def start_date_2(self):
        return "2025-11-25T00:00:00Z"
