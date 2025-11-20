import unittest

from parameterized import parameterized

from tap_sendwithus.utils import (get_datetime_fields_from_schema,
                                  get_datetime_from_timestamp,
                                  get_timestamp_from_datetime)

STANDARD_TEST_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": [
                "null",
                "integer"
            ]
        },
        "created_at": {
            "type": [
                "null",
                "string"
            ],
            "format": "date-time"
        },
        "updated_at": {
            "type": [
                "null",
                "string"
            ],
            "format": "date-time"
        }
    }
}

NESTED_TEST_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": [
                "null",
                "integer"
            ]
        },
        "profile": {
            "type": [
                "null",
                "object"
            ],
            "properties": {
                "birth_date": {
                    "type": [
                        "null",
                        "string"
                    ],
                    "format": "date-time"
                },
                "signup_date": {
                    "type": [
                        "null",
                        "string"
                    ],
                    "format": "date-time"
                }
            }
        },
        "events": {
            "type": [
                "null",
                "array"
            ],
            "items": {
                "type": [
                    "null",
                    "object"
                ],
                "properties": {
                    "event_date": {
                        "type": [
                            "null",
                            "string"
                        ],
                        "format": "date-time"
                    },
                    "event_type": {
                        "type": [
                            "null",
                            "string"
                        ]
                    }
                }
            }
        }
    }
}

NESTED_ARRAY_TEST_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": [
                "null",
                "integer"
            ]
        },
        "activities": {
            "type": [
                "null",
                "array"
            ],
            "items": {
                "type": [
                    "null",
                    "object"
                ],
                "properties": {
                    "activity_date": {
                        "type": [
                            "null",
                            "string"
                        ],
                        "format": "date-time"
                    },
                    "details": {
                        "type": [
                            "null",
                            "object"
                        ],
                        "properties": {
                            "last_updated": {
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "format": "date-time"
                            }
                        }
                    }
                }
            }
        }
    }
}


class TestUtils(unittest.TestCase):

    @parameterized.expand([
        ["none value", None, None],
        ["valid timestamp", 1625077800, "2021-06-30T18:30:00Z"],
    ])
    def test_datetime_from_timestamp(self, test_name, timestamp, expected):
        """Test the get_datetime_from_timestamp function."""

        result = get_datetime_from_timestamp(timestamp)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ["null value", None, None],
        ["valid datetime", "2021-06-30T18:30:00Z", 1625077800],
        ["valid bookmark datetime", "2021-12-01T10:15:30.000000Z", 1638353730],
    ])
    def test_get_timestamp_from_datetime(self, test_name, datetime_str, expected):
        """Test the get_timestamp_from_datetime function."""

        result = get_timestamp_from_datetime(datetime_str)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ["standard schema", STANDARD_TEST_SCHEMA, {"created_at", "updated_at"}],
        ["nested schema", NESTED_TEST_SCHEMA, {"birth_date", "signup_date", "event_date"}],
        ["nested array schema", NESTED_ARRAY_TEST_SCHEMA, {"activity_date", "last_updated"}],
    ])
    def test_get_datetime_fields_from_schema(self, test_name, schema, expected_datetime_fields):
        """Test the get_datetime_fields_from_schema function. This test will check various schema structures."""

        actual_datetime_fields = get_datetime_fields_from_schema(schema)
        self.assertEqual(actual_datetime_fields, expected_datetime_fields)
