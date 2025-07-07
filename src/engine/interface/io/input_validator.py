from engine.state.game_state import GameState
from lib.interface.events.moves.base_move import BaseMove
from lib.interface.events.moves.typing import MoveType
from lib.interface.queries.base_query import BaseQuery


class MoveValidator:
    def __init__(self, state: GameState):
        self.state = state

    def validate(self, record: MoveType, query: BaseQuery, player: int) -> None:
        self._validate_move(record, query, player)

    def _validate_move(self, r: BaseMove, query: BaseQuery, player: int) -> None:
        if not r.player_id == player:
            raise ValueError(
                "You set the move 'player_id' to a player_id other than your own."
            )
