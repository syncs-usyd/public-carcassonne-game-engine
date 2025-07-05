from lib.config.expansion import EXPANSION
from lib.interact.tile import Tile


class Meeple:
    """
    Meeple
    """

    placed = Tile | None

    def __init__(self, player_id: int, is_special: bool = False) -> None:
        if not EXPANSION:
            assert not self.is_special

        self.is_special = is_special
        self.player_id = id

    def _place_meeple(self, tile: Tile, edge: str):
        self.placed = tile
        tile.internal_edge_claims[edge] = self
