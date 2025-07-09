from lib.interface.queries.query_place_tile import QueryPlaceTile
from lib.interface.queries.query_place_meeple import QueryPlaceMeeple
from lib.interface.queries.typing import QueryType
from lib.interface.events.moves.move_place_meeple import (
    MovePlaceMeeple,
    MovePlaceMeeplePass,
)
from lib.interface.events.moves.move_place_tile import MovePlaceTile
from lib.interface.events.moves.typing import MoveType
from helper.client_state import ClientSate
from helper.state_mutator import StateMutator
from helper.interface import Connection


class Game:
    def __init__(self):
        self.state = ClientSate()
        self.mutator = StateMutator(self.state)
        self.connection = Connection()

    def get_next_query(self) -> QueryType:
        query = self.connection.get_next_query()

        new_events_mark = len(self.state.event_history)
        for i, record in query.update.items():
            self.mutator.commit(i, record)
        self.state.new_events = new_events_mark

        return query

    def send_move(self, move: MoveType) -> None:
        self.connection.send_move(move)

    def move_place_tile(
        self, query: QueryPlaceTile, tile, tile_index: int
    ) -> MovePlaceTile:
        return MovePlaceTile(
            player_id=self.state.me.player_id, tile=tile, player_tile_index=tile_index
        )

    def move_place_meeple(
        self, query: QueryPlaceMeeple, tile, placed_on: str
    ) -> MovePlaceMeeple:
        return MovePlaceMeeple(
            player_id=self.state.me.player_id, tile=tile, placed_on=placed_on
        )

    def move_place_meeple_pass(self, query: QueryPlaceMeeple) -> MovePlaceMeeplePass:
        return MovePlaceMeeplePass(
            player_id=self.state.me.player_id,
        )
