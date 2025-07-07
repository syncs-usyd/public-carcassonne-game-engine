from lib.interface.events.moves.move_place_tile import MovePlaceTile
from lib.interface.events.moves.move_place_meeple import MovePaceMeeple

from typing import Union

MoveType = Union[
    MovePlaceTile,
    MovePaceMeeple,
]
