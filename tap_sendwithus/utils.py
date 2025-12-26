from datetime import datetime, timezone
from typing import Optional

import singer

LOGGER = singer.get_logger()

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
BOOKMARK_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def get_timestamp_from_datetime(date_str: Optional[str]) -> Optional[int]:
    """Convert an ISO 8601 formatted date-time string to a timestamp in seconds.
    If the date_str is None, return None.

    Args:
        date_str (Optional[str]): The ISO 8601 formatted date-time string.

    Returns:
        Optional[int]: The timestamp in seconds.
    """

    if date_str is None:
        return None

    try:
        dt = datetime.strptime(date_str, DATETIME_FORMAT).replace(tzinfo=timezone.utc)
    except Exception:
        dt = datetime.strptime(date_str, BOOKMARK_FORMAT).replace(tzinfo=timezone.utc)

    return int(dt.timestamp())
