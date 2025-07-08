from engine.config.game_config import STARTING_POINTS
from engine.state.game_state import GameState

from lib.interface.events.event_game_started import (
    EventGameStarted,
)
from lib.interface.events.event_player_drew_cards import EventPlayerDrewCards
from lib.interface.events.typing import EventType
from lib.models.player_model import PublicPlayerModel


class CensorEvent:
    def __init__(self, state: GameState) -> None:
        self.state = state

    def censor(self, event: EventType, player_id: int) -> EventType:
        match event:
            case EventPlayerDrewCards() as e:
                if e.player_id == player_id:
                    return e

                return e.get_public()

            case EventGameStarted() as e:
                return e.get_public(
                    PublicPlayerModel(player_id=player_id, points=STARTING_POINTS)
                )

        return event
