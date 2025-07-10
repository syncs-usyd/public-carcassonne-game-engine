from lib.interact.tile import (
    Tile,
    create_base_tiles,
    create_river_tiles,
    # create_expansion_tiles,
)

from lib.config.map_config import MAP_CENTER, MAX_MAP_LENGTH


class Map:
    def __init__(self) -> None:
        self.placed_tiles: list[Tile] = []
        self.available_tiles: list[Tile] = []
        self._grid: list[list[Tile | None]] = [
            [None for _ in range(MAX_MAP_LENGTH)] for _ in range(MAX_MAP_LENGTH)
        ]
        self._grid_subscribers = []

    def start_base_phase(self) -> None:
        assert not self.available_tiles
        self.available_tiles.extend(create_base_tiles())

    def start_river_phase(self) -> None:
        assert not self.available_tiles

        starting_tile = Tile.get_starting_tile()

        self._grid[MAP_CENTER[1]][MAP_CENTER[0]] = starting_tile
        self.placed_tiles.append(starting_tile)
        starting_tile.placed_pos = MAP_CENTER

        self.available_tiles.extend(create_river_tiles())

    def add_expansion_pack(self, expansion_pack) -> None:
        pass
