from engine.config.game_config import NUM_MEEPLE

from lib.interact.meeple import Meeple


class PlayerState:
    def __init__(self, player_id: int) -> None:
        self.id = player_id
        self.points = 0
        self.cards = []
        self.meeples: list["Meeple"] = [Meeple(player_id) for _ in range(NUM_MEEPLE)]

    def _get_available_meeple(self) -> Meeple | None:
        available_meeples = [m for m in self.meeples if m.placed is not None]

        if available_meeples:
            return available_meeples[0]
 
        return None
