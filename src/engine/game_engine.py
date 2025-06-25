from engine.state.game_state import GameState

class GameEngine:
    def __init__(self):
        print("Intialising game engine!")

        self.state = GameState()
        # Logging
        # Output

    def run(self):
        print("Game Engine Live!")
