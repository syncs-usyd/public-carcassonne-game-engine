from lib.interface.events.base_event import BaseEvent

from typing import Literal


class EventPlayerBanned(BaseEvent):
    event_type: Literal["event_player_banned"] = "event_player_banned"
    player_id: int
    ban_type: int
    description: str
    # TODO add moves
