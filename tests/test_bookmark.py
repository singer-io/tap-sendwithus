from base import sendwithusBaseTest
from tap_tester.base_suite_tests.bookmark_test import BookmarkTest


class sendwithusBookMarkTest(BookmarkTest, sendwithusBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""
    bookmark_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    initial_bookmarks = {
        "bookmarks": {
            "templates": { "created" : "2020-01-01T00:00:00Z"},
            "logs": { "created" : "2020-01-01T00:00:00Z"},
            "log_events": { "created" : "2020-01-01T00:00:00Z"},
            "snippets": { "modified" : "2020-01-01T00:00:00Z"},
        }
    }
    @staticmethod
    def name():
        return "tap_tester_sendwithus_bookmark_test"

    def streams_to_test(self):
        streams_to_exclude = {}
        return self.expected_stream_names().difference(streams_to_exclude)

