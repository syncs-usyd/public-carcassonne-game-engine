from lib.interface.events.moves.base_move import BaseMove
from lib.interact.tile import Tile

from typing import Literal


class MovePaceTile(BaseMove):
    event_type: Literal["move_place_tile"] = "move_place_tile"
    player_id: int
    tile: Tile
    placed_on_tile: Tile
    placed_on_edge: str
