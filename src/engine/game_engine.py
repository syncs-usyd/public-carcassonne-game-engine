from engine.config.game_config import MAX_ROUNDS, NUM_CARDS_DRAWN_PER_ROUND, NUM_PLAYERS
from engine.interface.io.censor_event import CensorEvent
from engine.interface.io.input_validator import MoveValidator
from engine.state.game_state import GameState

from engine.state.player_state import PlayerState
from engine.state.state_mutator import StateMutator
from lib.config.expansion import EXPANSION

from random import sample

from lib.interface.events.event_game_started import EventGameStarted
from lib.interface.events.event_player_drew_cards import EventPlayerDrewCards


class GameEngine:
    def __init__(self):
        print("Intialising game engine!")

        self.state = GameState()
        self.validator = MoveValidator(self.state)
        self.mutator = StateMutator(self.state)
        self.censor = CensorEvent(self.state)
        # Logging
        # Output

    def run(self):
        assert NUM_PLAYERS == len(self.state.players)
        turn_order = sample(self.state.turn_order, k=NUM_PLAYERS)
        self.state.turn_order = turn_order

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
            self.mutator.commit(
                EventGameStarted(
                    turn_order=self.state.turn_order,
                    players=[
                        player._to_player_model() for player in self.state.players
                    ],
                )
            )

            for player_id in turn_order:
                player = self.state.players[player_id]
                cards_drawn = sample(
                    self.state.map.available_tiles, NUM_CARDS_DRAWN_PER_ROUND
                )

                for card in cards_drawn:
                    self.state.map.available_tiles.remove(card)

                player.cards.extend(cards_drawn)
                self.mutator.commit(
                    EventPlayerDrewCards(
                        player_id=player_id,
                        num_cards=2,
                        cards=[tile._to_model() for tile in player.cards],
                    )
                )

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
