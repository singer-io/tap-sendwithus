from tap_sendwithus.streams.abstracts import ParentBaseStream


class Logs(ParentBaseStream):
    tap_stream_id = "logs"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["created"]
    path = "logs"
    children = ["log_events"]
    http_method = "GET"
