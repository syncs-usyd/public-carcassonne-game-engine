from lib.interface.events.base_event import BaseEvent

from typing import Literal

from lib.models.tile_model import TileModel


class EventPlayerDrewCards(BaseEvent):
    event_type: Literal["event_player_drew_cards"] = "event_player_drew_cards"
    player_id: int
    num_cards: int
    cards: list[TileModel]

    def get_public(self) -> "PublicEventPlayerDrewCards":
        return PublicEventPlayerDrewCards(
            player_id=self.player_id, num_cards=self.num_cards
        )


class PublicEventPlayerDrewCards(BaseEvent):
    event_type: Literal["public_event_player_drew_cards"] = (
        "public_event_player_drew_cards"
    )
    player_id: int
    num_cards: int
