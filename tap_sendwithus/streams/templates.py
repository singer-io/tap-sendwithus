from tap_sendwithus.streams.abstracts import IncrementalStream

class Templates(IncrementalStream):
    tap_stream_id = "templates"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["created"]
    path = "templates"

