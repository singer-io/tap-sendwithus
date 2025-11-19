from datetime import datetime, timezone
from typing import Dict, List, Optional, Set

import singer

LOGGER = singer.get_logger()

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
BOOKMARK_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def get_datetime_from_timestamp(timestamp: Optional[int]) -> Optional[str]:
    """Convert a timestamp to an ISO 8601 formatted date-time string.
    If the timestamp is None, return None.

    Args:
        timestamp (Optional[int]): The timestamp in seconds.

    Returns:
        Optional[str]: The ISO 8601 formatted date-time string.
    """

    if timestamp is None:
        return None

    datetime_obj = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return datetime_obj.strftime(DATETIME_FORMAT)


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


def get_datetime_fields_from_schema(schema: Dict) -> Set[str]:
    """ Function to get datetime fields from the schema

    Args:
        schema (Dict): Schema specific to a stream

    Returns:
        Set[str]: Set of fields with format date-time
    """

    schema_properties = schema.get("properties", {})
    datetime_fields = set()

    for field, field_props in schema_properties.items():
        # First check the type of the field
        if field_props.get("format") == "date-time":
            # This is a date-time field, so add in the list
            datetime_fields.add(field)

        elif set(field_props.get("type", [])) == {"null", "object"}:
            # This can have nested date-time fields
            nested_props = {"properties": field_props.get("properties", {})}
            datetime_nested_fields = get_datetime_fields_from_schema(schema=nested_props)
            datetime_fields.update(datetime_nested_fields)

        elif set(field_props.get("type", [])) == {"null", "array"}:
            # This can have nested date-time fields in items
            items_props = {"properties": field_props.get("items", {}).get("properties", {})}
            datetime_nested_fields = get_datetime_fields_from_schema(schema=items_props)
            datetime_fields.update(datetime_nested_fields)

    return datetime_fields


def sort_records_by_replication_key(records: List[Dict], replication_key: str) -> List[Dict]:
    """ Function to sort records by replication key in ascending order

    Args:
        records (list): List of records to be sorted
        replication_key (str): Replication key to sort the records

    Returns:
        list: Sorted list of records
    """

    return sorted(
        records,
        key=lambda record: record.get(replication_key)
    )
