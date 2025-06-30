from engine.config.game_config import NUM_PLAYERS
from engine.state.player_state import PlayerState

from lib.interact.tile import Tile, TileModifier
from lib.interact.map import Map


class GameState:
    def __init__(self):
        self.round = -1
        self.players = [PlayerState(i) for i in range(NUM_PLAYERS)]
        self.map = Map()

        self.game_over = False

        self.placed_tiles = []
        self.river_tiles = []
        self.regular_tiles = []

    def start_new_round(self) -> None:
        pass

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
        self.placed_tiles.append(card)

        if TileModifier.RIVER in card.modifier:
            self.river_tiles.remove(card)
            return

        self.regular_tiles.remove(card)
        #TODO record event

    def place_meeple(self, player: "PlayerState", tile: "Tile") -> None
        pass

    def _check_reward(self) -> None:
        pass

