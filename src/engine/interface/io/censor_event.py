from typing import TYPE_CHECKING

from lib.interface.events.event_game_started import (
    EventGameStarted,
    PublicEventGameStarted,
)
from lib.interface.events.event_player_drew_cards import EventPlayerDrewCards
from lib.interface.events.typing import EventType

if TYPE_CHECKING:
    from engine.state.game_state import GameState


class CensorEvent:
    def __init__(self, state: "GameState") -> None:
        self.state = state

    def censor(self, event: EventType, player_id: int) -> EventType:
        match event:
            case EventPlayerDrewCards() as e:
                if e.player_id == player_id:
                    return e

                return e.get_public()

            case EventGameStarted() as e:
                return PublicEventGameStarted(
                    turn_order=e.turn_order,
                    players=[player.get_public() for player in e.players],
                    you=filter(
                        lambda x: x.player_id == player_id, e.players
                    ).__next__(),
                )

        return event
