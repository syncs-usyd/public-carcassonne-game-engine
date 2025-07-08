from lib.interface.events.moves.base_move import BaseMove
from lib.interact.tile import Tile

from typing import Literal


class MovePlaceMeeple(BaseMove):
    event_type: Literal["move_place_meeple"] = "move_place_meeple"
    player_id: int
    tile: Tile
    placed_on: str  # EDGES or MONESTARY


class MovePlaceMeeplePass(BaseMove):
    event_type: Literal["move_place_meeple_pass"] = "move_place_meeple_pass"
    player_id: int
