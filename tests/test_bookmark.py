from base import SendwithusBaseTest
from tap_tester.base_suite_tests.bookmark_test import BookmarkTest
from datetime import datetime, timedelta, timezone


class SendwithusBookMarkTest(BookmarkTest, SendwithusBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""
    bookmark_format = "%Y-%m-%dT%H:%M:%SZ"
    initial_bookmarks = {
        "bookmarks": {
            "templates": {"created": "2020-01-01T00:00:00Z"},
            "logs": {"created": "2020-01-01T00:00:00Z"},
            "log_events": {"created": "2020-01-01T00:00:00Z"},
            "snippets": {"modified": "2020-01-01T00:00:00Z"},
        }
    }

    @staticmethod
    def name():
        return "tap_tester_sendwithus_bookmark_test"

    def streams_to_test(self):
        streams_to_exclude = {"drip_campaigns"}  # Excluding drip_campaigns since it uses full table replication
        return self.expected_stream_names().difference(streams_to_exclude)

    def calculate_new_bookmarks(self):
        """Calculates new bookmarks by looking through sync 1 data to determine
        a bookmark that will sync 2 records in sync 2 (plus any necessary look
        back data)"""
        # NOTE: The timestamps for logs and log_events needs to be updated since the test data will get deleted after 7 days.
        # If the test fails, create new logs and log_events by using the script `generate-logs-data.py` present in spikes

        delta = timedelta(hours=12)
        now_minus_1_day = (datetime.now(tz=timezone.utc) - delta).isoformat(timespec="seconds").replace("+00:00", "Z")

        new_bookmarks = {
            "templates": {"created": "2025-11-11T00:00:00Z"},
            "logs": {"created": now_minus_1_day},
            "log_events": {"created": now_minus_1_day},
            "snippets": {"modified": "2025-11-11T06:25:22Z"},
        }

        return new_bookmarks
