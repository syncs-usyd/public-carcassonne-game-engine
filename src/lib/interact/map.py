from lib.interact.tile import Tile


class Map:
    def __init__(self) -> None:
        self.placed_tiles = [Tile.get_start_tile()]
        self.available_tiles = []
        self.feature_set: dict[Tile, list[Tile]]
