from engine.config.game_config import MAX_ROUNDS, NUM_CARDS_DRAWN_PER_ROUND, NUM_PLAYERS
from engine.interface.io.input_validator import MoveValidator
from engine.state.game_state import GameState

from engine.state.player_state import PlayerState
from engine.state.state_mutator import StateMutator
from lib.config.expansion import EXPANSION

from random import sample


class GameEngine:
    def __init__(self):
        print("Intialising game engine!")

        self.state = GameState()
        self.validator = MoveValidator(self.state)
        self.mutator = StateMutator(self.state)
        self.censor = None
        # Logging
        # Output

    def run(self):
        assert NUM_PLAYERS == len(self.state.players)
        turn_order = sample(self.state.players, k=NUM_PLAYERS)

        while not self.state.is_game_over():
            print(f"New round {self.state.round + 1}")

            if self.state.round == -1:
                self.state.start_river_phase()

            if self.state.cards_exhausted:
                self.state.replinish_player_cards()

                if self.state.round != -1:
                    self.state.start_base_phase()
                    if EXPANSION:
                        self.state.extend_base_phase()

            self.state.start_new_round()

            for player in turn_order:
                cards_drawn = sample(
                    self.state.map.available_tiles, NUM_CARDS_DRAWN_PER_ROUND
                )

                for card in cards_drawn:
                    self.state.map.available_tiles.remove(card)

                player.cards.extend(cards_drawn)

                self.start_player_turn(player)

            if self.state.round > MAX_ROUNDS or any(
                [p >= 50 for p in self.state.get_player_points()]
            ):
                self.state.finalise_game()

    def start_player_turn(self, player: PlayerState) -> None:
        response = player.connection.query_place_tile(
            self.state, self.validator, self.censor
        )
        self.mutator.commit(response)

        response = player.connection.query_place_meeple(
            self.state, self.validator, self.censor
        )
        self.mutator.commit(response)

        # record this
