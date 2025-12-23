import unittest

from parameterized import parameterized

from tap_sendwithus.utils import get_timestamp_from_datetime


class TestUtils(unittest.TestCase):

    @parameterized.expand([
        ["null value", None, None],
        ["valid datetime", "2021-06-30T18:30:00Z", 1625077800],
        ["valid bookmark datetime", "2021-12-01T10:15:30.000000Z", 1638353730],
    ])
    def test_get_timestamp_from_datetime(self, test_name, datetime_str, expected):
        """Test the get_timestamp_from_datetime function."""

        result = get_timestamp_from_datetime(datetime_str)
        self.assertEqual(result, expected)
