from tap_sendwithus.streams.templates import Templates
from tap_sendwithus.streams.logs import Logs
from tap_sendwithus.streams.log_events import LogEvents
from tap_sendwithus.streams.snippets import Snippets
from tap_sendwithus.streams.drip_campaigns import DripCampaigns

STREAMS = {
    "templates": Templates,
    "logs": Logs,
    "log_events": LogEvents,
    "snippets": Snippets,
    "drip_campaigns": DripCampaigns,
}

