from tap_sendwithus.streams.abstracts import IncrementalStream

class Snippets(IncrementalStream):
    tap_stream_id = "snippets"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["modified"]
    path = "snippets"

