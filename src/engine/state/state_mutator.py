from engine.state.game_state import GameState
from lib.interface.events.moves.move_place_meeple import (
    MovePlaceMeeple,
    MovePlaceMeeplePass,
)
from lib.interface.events.moves.move_place_tile import MovePlaceTile
from lib.interface.events.moves.typing import MoveType


class StateMutator:
    def __init__(self, state: GameState) -> None:
        self.state = state

    def commit(self, move: MoveType):
        match move:
            case MovePlaceTile() as r:
                self._commit_place_tile(r)

            case MovePlaceMeeple() as r:
                self._commit_place_meeple(r)

    def _commit_place_tile(self, move: MovePlaceTile) -> None:
        # Get tile from player hand
        tile = self.state.players[move.player_id].cards[move.tile.player_tile_index]
        self.state.map._grid[move.pos[0]][move.pos[1]] = tile

        # Keep track of tile placed for meeple placement
        self.state.tile_placed = tile
        tile.pos = move.pos

        # Check for any complete connected componentes
        completed_components = self.state.check_any_complete(tile)

        for edge in completed_components:
            reward = self.state._get_reward(tile, edge)

            for player_id in self.state._get_claims(tile, edge):
                player = self.state._get_player_from_id(player_id)

                if player:
                    player.points += reward

            meeples_to_return = list(
                self.state._traverse_connected_component(
                    tile,
                    edge,
                    yield_cond=lambda t, e: t.internal_edge_claims[edge] is not None,
                )
            )

            # TODO Record, may change this into a functional
            for t, e in meeples_to_return:
                t.internal_edge_claims[e] = None

    def _commit_place_meeple(self, move: MovePlaceMeeple) -> None:
        player = self.state.players[move.player_id]
        assert self.state.tile_placed

        # TODO linked to monesteryt issue below
        self.state.tile_placed.internal_edge_claims[move.edge] = move.player_id

        completed_components = self.state.check_any_complete(self.state.tile_placed)

        # TODO implement monestery functional modifier
        if move.placed_on == "MONESTERY":
            pass

        elif move.placed_on in completed_components:
            player.points += self.state._get_reward(
                self.state.tile_placed, move.placed_on
            )

        self.state.tile_placed = None

    def _commit_place_meeple_pass(self, move: MovePlaceMeeplePass) -> None:
        self.state.tile_placed = None
