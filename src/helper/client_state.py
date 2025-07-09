from lib.config.map_config import MAX_MAP_LENGTH
from lib.interact.meeple import Meeple
from lib.interact.map import Map
from lib.interface.events.typing import EventType
from lib.models.player_model import PlayerModel, PublicPlayerModel


class ClientSate:
    def __init__(self):
        self.round = -1
        self.players: dict[int, PublicPlayerModel]
        self.map = Map()

        self.game_over = False
        self.num_placed_cards = 0

        self.event_history: list["EventType"] = []
        self.new_events: int = 0
        self.turn_order: list[int] = []

        self.points = 0
        self.me: PlayerModel

    def get_meeples_placed_by(self, player_id: int | None) -> list[Meeple]:
        """
        Get Meeples Placed
        Giving None as player id retruns all placed meeples
        """
        meeples = []
        for x in range(MAX_MAP_LENGTH):
            for y in range(MAX_MAP_LENGTH):
                tile = self.map._grid[y][x]

                if tile is None:
                    continue

                for edge, meeple in tile.internal_claims.items():
                    if meeple and (meeple.player_id == player_id or not player_id):
                        meeples.append(meeple)

        return meeples
