from lib.interface.events.event_game_ended import (
    EventGameEndedCancelled,
    EventGameEndedPointLimitReaced,
    EventGameEndedStaleMate,
)
from lib.interface.events.event_game_started import (
    EventGameStarted,
    PublicEventGameStarted,
)
from lib.interface.events.event_meeple_placed import EventMeeplePlaced
from lib.interface.events.event_player_bannned import EventPlayerBanned
from lib.interface.events.event_player_drew_cards import (
    EventPlayerDrewCards,
    PublicEventPlayerDrewCards,
)
from lib.interface.events.event_player_meeple_freed import EventPlayerMeepleFreed
from lib.interface.events.event_player_turn_started import EventPlayerTurnStarted
from lib.interface.events.event_player_won import EventPlayerWon
from lib.interface.events.event_river_phase_completed import EventRiverPhaseCompleted
from lib.interface.events.event_structure_completed import EventStructureCompleted
from lib.interface.events.moves.typing import MoveType

from typing import Union

EventType = Union[
    EventGameStarted,
    EventMeeplePlaced,
    EventPlayerBanned,
    EventPlayerDrewCards,
    EventPlayerTurnStarted,
    EventPlayerWon,
    EventRiverPhaseCompleted,
    EventStructureCompleted,
    EventPlayerMeepleFreed,
    EventPlayerWon,
    EventGameEndedCancelled,
    EventGameEndedPointLimitReaced,
    EventGameEndedStaleMate,
    PublicEventGameStarted,
    PublicEventPlayerDrewCards,
    MoveType,
]
