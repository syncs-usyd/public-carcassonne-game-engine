from lib.interface.events.base_event import BaseEvent

from typing import Literal


class EventPlayerMetPointLimit(BaseEvent):
    event_type: Literal["event_player_met_point_limit"] = "event_player_met_point_limit"
    player_id: int
