from base import SendwithusBaseTest
from tap_tester.base_suite_tests.bookmark_test import BookmarkTest
from datetime import datetime, timedelta, timezone


class SendwithusBookMarkTest(BookmarkTest, SendwithusBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""
    bookmark_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    initial_bookmarks = {
        "bookmarks": {
            "templates": {"created": "2020-01-01T00:00:00.000000Z"},
            "logs": {"created": "2020-01-01T00:00:00.000000Z"},
            "log_events": {"created": "2020-01-01T00:00:00.000000Z"},
            "snippets": {"modified": "2020-01-01T00:00:00.000000Z"},
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
        # Generate data 2 times with a gap of few mins between them to have consistent test results as start_date_2 is having a delta of 5 mins. 

        lookback = timedelta(minutes=10)

        def _subtract_lookback(stream, replication_key):
            """Reads the max bookmark for a stream from sync 1 state
            and subtracts the lookback window."""
            state_bookmarks = (BookmarkTest.state_1 or {}).get("bookmarks", {})
            raw = state_bookmarks.get(stream, {}).get(replication_key)
            if raw:
                bookmark_dt = datetime.strptime(
                    raw, self.bookmark_format
                ).replace(tzinfo=timezone.utc)
                return (bookmark_dt - lookback).strftime(self.bookmark_format)
            # Fallback: use now minus lookback if state is unavailable
            return (
                datetime.now(tz=timezone.utc) - lookback
            ).strftime(self.bookmark_format)

        new_bookmarks = {
            "templates": {"created": "2025-11-11T00:00:00.000000Z"},
            "logs": {
                "created": _subtract_lookback("logs", "created")
            },
            "log_events": {
                "created": _subtract_lookback("log_events", "created")
            },
            "snippets": {"modified": "2025-11-11T06:25:22.000000Z"},
        }

        return new_bookmarks
