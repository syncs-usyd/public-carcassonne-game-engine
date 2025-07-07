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

    def _commit_place_tile(self, move: MovePlaceTile):
        tile = self.state.players[move.player_id].cards[move.tile.player_tile_index]
        self.state.map._grid[move.pos[0]][move.pos[1]] = tile

        completed_components = self.state.check_any_complete(tile)

        for edge in completed_components:
            reward = self.state._get_reward(tile, edge)

            for player_id in self.state._get_claims(tile, edge):
                player = self.state._get_player_from_id(player_id)

                if player:
                    player.points += reward

    def _commit_place_meeple(self, move: MovePlaceMeeple):
        pass

    def _commit_place_meeple_pass(self, move: MovePlaceMeeplePass):
        pass
