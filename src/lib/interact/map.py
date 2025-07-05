from lib.interact.tile import (
    Tile,
    create_base_tiles,
    create_river_tiles,
    # create_expansion_tiles,
)


class Map:
    def __init__(self) -> None:
        self.placed_tiles = []
        self.available_tiles = []
        self.feature_set: dict[Tile, list[Tile]]

    def start_base_phase(self) -> None:
        assert not self.available_tiles
        self.available_tiles.extend(create_base_tiles())

    def start_river_phase(self) -> None:
        assert not self.available_tiles

        # TODO Record tile placment
        self.placed_tiles.append(Tile.get_starting_tile())
        self.available_tiles.extend(create_river_tiles())
