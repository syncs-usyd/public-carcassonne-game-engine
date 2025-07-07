from lib.interface.events.moves.base_move import BaseMove
from lib.models.tile_model import TileModel

from typing import Literal


class MovePlaceTile(BaseMove):
    event_type: Literal["move_place_tile"] = "move_place_tile"
    player_id: int
    tile: TileModel
    pos: tuple[int, int]
    rotation: int
