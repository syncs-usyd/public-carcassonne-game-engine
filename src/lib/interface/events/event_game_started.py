from lib.interface.events.base_event import BaseEvent

from typing import Literal, Sequence

from lib.models.player_model import PublicPlayerModel


class EventGameStarted(BaseEvent):
    event_type: Literal["event_game_started"] = "event_game_started"
    turn_order: list[int]
    players: Sequence[PublicPlayerModel]

    def get_public(self, player: PublicPlayerModel) -> "PublicEventGameStarted":
        return PublicEventGameStarted(
            turn_order=self.turn_order,
            players=self.players,
            player=player,
        )


class PublicEventGameStarted(BaseEvent):
    event_type: Literal["public_event_game_started"] = "public_event_game_started"
    turn_order: list[int]
    player: PublicPlayerModel
    players: Sequence[PublicPlayerModel]
