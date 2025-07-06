from lib.interface.events.base_event import BaseEvent

from typing import Literal


class EventGameStarted(BaseEvent):
    event_type: Literal["event_game_started"] = "event_game_started"
    turn_order: list[int]
