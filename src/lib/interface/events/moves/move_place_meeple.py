from lib.interface.events.moves.base_move import BaseMove
from lib.interact.tile import Tile

from typing import Literal


class MovePaceMeeple(BaseMove):
    event_type: Literal["move_place_meeple"] = "move_place_meeple"
    player_id: int
    tile: Tile
    placed_on_edge: str
