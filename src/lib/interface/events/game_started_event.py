from lib.interface.events.base_event import BaseEvent

from typing import Literal

class GameStartedEvent(BaseEvent):
    event_type: Literal["game_started_event"] = "game_started_event"
