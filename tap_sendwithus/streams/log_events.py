from tap_sendwithus.streams.abstracts import ChildBaseStream

class LogEvents(ChildBaseStream):
    tap_stream_id = "log_events"
    key_properties = ["status", "created"]
    replication_method = "INCREMENTAL"
    replication_keys = ["created"]
    path = "logs/(:log_id)/events"
    parent = "logs"
    bookmark_value = None

