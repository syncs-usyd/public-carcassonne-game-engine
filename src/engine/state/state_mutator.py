from engine.game.tile_subscriber import MonastaryNeighbourSubsciber
from engine.state.game_state import GameState

from lib.config.map_config import MONASTARY_IDENTIFIER
from lib.interface.events.moves.move_place_meeple import (
    MovePlaceMeeple,
    MovePlaceMeeplePass,
)
from lib.interface.events.moves.move_place_tile import MovePlaceTile
from lib.interface.events.typing import EventType


class StateMutator:
    def __init__(self, state: GameState) -> None:
        self.state = state

    def commit(self, event: EventType):
        self.state.event_history.append(event)

        match event:
            case MovePlaceTile() as r:
                self._commit_place_tile(r)

            case MovePlaceMeeple() as r:
                self._commit_place_meeple(r)

    def _commit_place_tile(self, move: MovePlaceTile) -> None:
        # Get tile from player hand
        tile = self.state.players[move.player_id].cards[move.player_tile_index]
        self.state.map._grid[move.tile.pos[1]][move.tile.pos[0]] = tile
        self.state.map.placed_tiles.append(tile)

        # Keep track of tile placed for meeple placement
        self.state.tile_placed = tile
        tile.placed_pos = move.tile.pos

        # Check for any complete connected componentes
        completed_components = self.state.check_any_complete(tile)

        # Check for base/regular connected components
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
                    yield_cond=lambda t, e: t.internal_claims[edge] is not None,
                )
            )

            # TODO Record, may change this into a functional
            for t, e in meeples_to_return:
                t.internal_claims[e] = None

        # Check for monastary/special completed componentes
        for subscibed_complete in self.state.tile_publisher.check_notify(tile):
            for player_id, reward, t, reward_edge in subscibed_complete._reward():
                self.state.players[player_id].points += reward

                # TODO record
                t.internal_claims[reward_edge] = None

    def _commit_place_meeple(self, move: MovePlaceMeeple) -> None:
        player = self.state.players[move.player_id]
        assert self.state.tile_placed

        self.state.tile_placed.internal_claims[move.placed_on] = move.player_id

        completed_components = self.state.check_any_complete(self.state.tile_placed)

        # This segment checks if player placed a meeple on a completed tile
        if move.placed_on == MONASTARY_IDENTIFIER:
            tile_subsciber = MonastaryNeighbourSubsciber(
                move.tile.pos, player.id, self.state.tile_placed, move.placed_on
            )
            tile_subsciber.register_to(self.state.tile_publisher)

            for subscibed_complete in self.state.tile_publisher.check_notify(
                self.state.tile_placed
            ):
                for player_id, reward, t, e in subscibed_complete._reward():
                    self.state.players[player_id].points += reward
                    assert player_id == move.player_id

                    # TODO record
                    t.internal_claims[e] = None

        # Check the player completed a reguar component and claimed
        elif move.placed_on in completed_components:
            player.points += self.state._get_reward(
                self.state.tile_placed, move.placed_on
            )

        # Cleanup intermeidate state variables
        self.state.tile_placed = None

    def _commit_place_meeple_pass(self, move: MovePlaceMeeplePass) -> None:
        # Cleanup intermeidate state variables
        self.state.tile_placed = None

    def _check_subscibers(self) -> None:
        pass
