from engine.config.expansion_config import EXPANSION_PACKS
from engine.config.game_config import NUM_PLAYERS, NUM_CARDS_IN_HAND
from engine.game.tile_subscriber import TilePublisherBus
from engine.interface.io.player_connection import PlayerConnection
from engine.state.player_state import PlayerState

from lib.interact.tile import Tile, TileModifier
from lib.interact.map import Map
from lib.interface.events.typing import EventType

from typing import Callable, Generator
from collections import deque
from random import sample


class GameState:
    def __init__(self):
        self.round = -1
        self.players = [PlayerState(i, PlayerConnection(i)) for i in range(NUM_PLAYERS)]
        self.map = Map()

        self.game_over = False
        self.cards_exhausted = True

        self.tile_placed: Tile | None = None
        self.tile_publisher = TilePublisherBus()

        self.event_history: list[EventType] = []
        self.turn_order: list[int] = [player.id for player in self.players]

    def replinish_player_cards(self) -> None:
        for player in self.players:
            player.cards.extend(sample(self.map.available_tiles, NUM_CARDS_IN_HAND))

    def start_river_phase(self) -> None:
        self.map.start_river_phase()

    def start_base_phase(self) -> None:
        self.map.start_base_phase()

    def extend_base_phase(self) -> None:
        for ex in EXPANSION_PACKS:
            self.map.add_expansion_pack(ex)

    def start_new_round(self) -> None:
        self.round += 1

    def get_player_points(self) -> list[int]:
        return [player.points for player in self.players]

    def is_game_over(self) -> bool:
        return self.game_over

    def finalise_game(self) -> None:
        self.game_over = True
        self.calc_final_points()

    def calc_final_points(self):
        pass

    def _get_claims(self, tile: "Tile", edge: str) -> list[int]:
        players = set()

        for connected_tile, _ in self._traverse_connected_component(tile, edge):
            edge_claim = connected_tile.internal_claims[edge]
            if edge_claim != -1:
                players.add(edge_claim)

        return list(players)

    def _get_reward(self, tile: "Tile", edge: str) -> int:
        visited_tiles = set()
        structure_type = tile.internal_edges[edge]

        total_points = 0

        for connected_tile, _ in self._traverse_connected_component(tile, edge):
            if connected_tile in visited_tiles:
                continue

            visited_tiles.add(connected_tile)
            total_points += TileModifier.apply_point_modifiers(structure_type)

        return total_points

    def _check_completed_component(self, start_tile: Tile, edge: str) -> bool:
        component = list(self._traverse_connected_component(start_tile, edge))

        for tile, edge in component:
            if tile.external_edges[edge] is None:
                return False

        return True

    def check_any_complete(self, start_tile: "Tile") -> list[str]:
        edges_complete: list[str] = []
        for edge, tile in start_tile.external_edges.items():
            if self._check_completed_component(tile, edge):
                edges_complete.append(edge)

        return edges_complete

    def _get_player_from_id(self, id: int) -> PlayerState | None:
        for player in self.players:
            if player.id == id:
                return player

        return None

    def _traverse_connected_component(
        self,
        start_tile: "Tile",
        edge: str,
        yield_cond: Callable[[Tile, str], bool] = lambda _1, _2: True,
        modify: Callable[[Tile, str], None] = lambda _1, _2: None,
    ) -> Generator[tuple["Tile", str]]:
        visited = set()
        structure_type = start_tile.internal_edges[edge]
        structure_bridge = TileModifier.get_bridge_modifier(structure_type)

        queue = deque([(start_tile, edge)])

        while queue:
            tile, edge = queue.popleft()

            if (tile, edge) in visited:
                continue

            # Visiting portion of traversal
            visited.add((tile, edge))
            modify(tile, edge)

            if yield_cond(tile, edge):
                yield tile, edge

            connected_internal_edges = []

            for adjacent_edge in Tile.adjacent_edges(edge):
                if tile.internal_edges[adjacent_edge] == structure_type:
                    connected_internal_edges.append(adjacent_edge)

            if (
                not connected_internal_edges
                and structure_bridge
                and structure_bridge in tile.modifiers
            ):
                if tile.internal_edges[Tile.get_opposite(edge)] == structure_type:
                    connected_internal_edges.append(Tile.get_opposite(edge))

            for cid in connected_internal_edges:
                # neighbouring_tile = tile.external_edges[cid] TODO
                assert tile.placed_pos is not None
                neighbouring_tile = Tile.get_external_tile(
                    cid, tile.placed_pos, self.map._grid
                )

                if neighbouring_tile:
                    neighbouring_tile_edge = tile.get_opposite(cid)

                    if (neighbouring_tile, neighbouring_tile_edge) not in visited:
                        queue.append((neighbouring_tile, neighbouring_tile_edge))
