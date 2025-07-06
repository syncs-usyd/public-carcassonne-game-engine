from lib.interface.events.event_game_started import EventGameStarted
from lib.interface.events.event_meeple_placed import EventMeeplePlaced
from lib.interface.events.event_player_bannned import EventPlayerBanned
from lib.interface.events.event_player_drew_cards import EventPlayerDrewCards
from lib.interface.events.event_player_turn_started import EventPlayerTurnStarted
from lib.interface.events.event_player_won import EventPlayerWon
from lib.interface.events.event_river_phase_completed import EventRiverPhaseCompleted
from lib.interface.events.event_structure_completed import EventStructureCompleted
from lib.interface.events.event_player_met_point_limit import EventPlayerMetPointLimit

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
    EventPlayerMetPointLimit,
]
