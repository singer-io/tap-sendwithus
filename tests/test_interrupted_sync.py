from base import SendwithusBaseTest
from tap_tester.base_suite_tests.interrupted_sync_test import InterruptedSyncTest


class SendwithusInterruptedSyncTest(InterruptedSyncTest, SendwithusBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""

    @staticmethod
    def name():
        return "tap_tester_sendwithus_interrupted_sync_test"

    def streams_to_test(self):
        streams_to_exclude = {"drip_campaigns"}  # Excluding drip_campaigns since it uses full table replication
        return self.expected_stream_names().difference(streams_to_exclude)

    def manipulate_state(self):
        return {
            "currently_syncing": "templates",
            "bookmarks": {
                "templates": {"created": "2020-11-11T00:00:00Z"},
                "logs": {"created": "2020-11-18T00:00:00Z"},
                "log_events": {"created": "2020-11-18T00:00:00Z"},
                "snippets": {"modified": "2020-11-11T06:25:22Z"},
            }
        }
