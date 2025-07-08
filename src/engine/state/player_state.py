from engine.config.game_config import NUM_MEEPLE
from engine.interface.io.player_connection import PlayerConnection

from lib.interact.meeple import Meeple
from lib.interact.tile import Tile
from lib.models.player_model import PublicPlayerModel


class PlayerState:
    def __init__(self, player_id: int, connection: PlayerConnection) -> None:
        self.id = player_id
        self.points = 0
        self.cards: list[Tile] = []
        self.meeples: list["Meeple"] = [Meeple(player_id) for _ in range(NUM_MEEPLE)]
        self.connection = connection

    def _get_available_meeple(self) -> Meeple | None:
        available_meeples = [m for m in self.meeples if m.placed is not None]

        if available_meeples:
            return available_meeples[0]

        return None

    def _to_player_model(self) -> PublicPlayerModel:
        return PublicPlayerModel(player_id=self.id, points=self.points)
