from lib.interface.events.base_event import BaseEvent

from typing import Literal


class EventPlayerDrewCards(BaseEvent):
    event_type: Literal["event_player_drew_cards"] = "event_player_drew_cards"
    player_id: int
    num_cards: int
    cards: list[int]
