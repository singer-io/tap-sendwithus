from tap_sendwithus.streams.abstracts import FullTableStream


class DripCampaigns(FullTableStream):
    tap_stream_id = "drip_campaigns"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    path = "drip_campaigns"
    http_method = "GET"
