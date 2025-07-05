from engine.config.expansion import EXPANSION_PACKS
from engine.config.game_config import NUM_PLAYERS
from engine.state.player_state import PlayerState

from lib.interact.tile import Tile, TileModifier
from lib.interact.map import Map

from typing import Generator
from collections import deque


class GameState:
    def __init__(self):
        self.round = -1
        self.players = [PlayerState(i) for i in range(NUM_PLAYERS)]
        self.map = Map()

        self.game_over = False

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

    def place_card(self, player: "PlayerState", card: "Tile") -> None:
        self.map.placed_tiles.append(card)
        self.map.available_tiles.remove(card)
        # TODO record event

    def place_meeple(self, player: "PlayerState", tile: "Tile", edge: str) -> None:
        meeple = player._get_available_meeple()
        assert meeple is not None

        meeple._place_meeple(tile, edge)

    def _get_claims(self, tile: "Tile", edge: str) -> list[int]:
        players = set()

        for connected_tile, _ in self._traverse_connected_component(tile, edge):
            edge_claim = connected_tile.internal_edge_claims[edge]
            if edge_claim != -1:
                players.add(edge_claim)

        return list(players)

    def _get_reward(self, player: "PlayerState", tile: "Tile", edge: str) -> int:
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

    def _traverse_connected_component(
        self,
        start_tile: "Tile",
        edge: str,
    ) -> Generator[tuple["Tile", str]]:
        visited = set()
        structure_type = start_tile.internal_edges[edge]
        structure_bridge = TileModifier.get_bridge_modifier(structure_type)

        queue = deque([(start_tile, edge)])

        while queue:
            tile, edge = queue.popleft()

            if (tile, edge) in visited:
                continue

            visited.add((tile, edge))
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
                neighbouring_tile = tile.external_edges[cid]

                if neighbouring_tile:
                    neighbouring_tile_edge = tile.get_opposite(cid)

                    if (neighbouring_tile, neighbouring_tile_edge) not in visited:
                        queue.append((neighbouring_tile, neighbouring_tile_edge))
