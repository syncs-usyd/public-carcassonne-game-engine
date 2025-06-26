from engine.config.game_config import NUM_PLAYERS
from engine.state.player_state import PlayerState

from lib.map import Map


class GameState:
    def __init__(self):
        self.round = -1
        self.players = [PlayerState(i) for i in range(NUM_PLAYERS)]
        self.map = Map()

        self.game_over = False

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
