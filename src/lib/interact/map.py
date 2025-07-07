from lib.interact.tile import (
    Tile,
    create_base_tiles,
    create_river_tiles,
    # create_expansion_tiles,
)

from lib.config.map_config import MAX_MAP_LENGTH


class Map:
    def __init__(self) -> None:
        self.placed_tiles = []
        self.available_tiles = []
        self._grid: list[list[Tile | None]] = [
            [None for _ in range(MAX_MAP_LENGTH)] for _ in range(MAX_MAP_LENGTH)
        ]

    def start_base_phase(self) -> None:
        assert not self.available_tiles
        self.available_tiles.extend(create_base_tiles())

    def start_river_phase(self) -> None:
        assert not self.available_tiles

        # TODO Record tile placment
        self.placed_tiles.append(Tile.get_starting_tile())
        self.available_tiles.extend(create_river_tiles())

    def add_expansion_pack(self, expansion_pack) -> None:
        pass
