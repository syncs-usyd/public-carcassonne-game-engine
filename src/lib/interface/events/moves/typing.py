from lib.interface.events.moves.move_place_tile import MovePaceTile
from lib.interface.events.moves.move_place_meeple import MovePaceMeeple

from typing import Union

MoveType = Union[
    MovePaceTile,
    MovePaceMeeple,
]
