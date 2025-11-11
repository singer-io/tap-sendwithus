
from base import sendwithusBaseTest
from tap_tester.base_suite_tests.interrupted_sync_test import InterruptedSyncTest


class sendwithusInterruptedSyncTest(sendwithusBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""

    @staticmethod
    def name():
        return "tap_tester_sendwithus_interrupted_sync_test"

    def streams_to_test(self):
        return self.expected_stream_names()


    def manipulate_state(self):
        return {
            "currently_syncing": "prospects",
            "bookmarks": {
                "templates": { "created" : "2020-01-01T00:00:00Z"},
                "logs": { "created" : "2020-01-01T00:00:00Z"},
                "log_events": { "created" : "2020-01-01T00:00:00Z"},
                "snippets": { "modified" : "2020-01-01T00:00:00Z"},
        }
    }

