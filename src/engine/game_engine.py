from engine.config.game_config import MAX_ROUNDS
from engine.state.game_state import GameState


class GameEngine:
    def __init__(self):
        print("Intialising game engine!")

        self.state = GameState()
        # Logging
        # Output

    def run(self):
        # turn_order = list(self.state.players)

        while not self.state.is_game_over():
            print(f"New round {self.state.round + 1}")
            self.state.start_new_round

            if self.state.round > MAX_ROUNDS or any(
                [p >= 50 for p in self.state.get_player_points()]
            ):
                self.state.finalise_game()
