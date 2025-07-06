from engine.config.game_config import MAX_ROUNDS, NUM_CARDS_DRAWN_PER_ROUND, NUM_PLAYERS
from engine.state.game_state import GameState

from lib.config.expansion import EXPANSION
from lib.interact.tile import Tile

from random import sample


class GameEngine:
    def __init__(self):
        print("Intialising game engine!")

        self.state = GameState()
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
                player.cards.append(
                    sample(self.state.map.available_tiles, NUM_CARDS_DRAWN_PER_ROUND)
                )

                # wait for player to place card
                placeholder_tile_placed: Tile = Tile.get_starting_tile()

                completed_components = self.state.check_any_complete(
                    placeholder_tile_placed
                )

                for edge in completed_components:
                    reward = self.state._get_reward(placeholder_tile_placed, edge)

                    for player_id in self.state._get_claims(
                        placeholder_tile_placed, edge
                    ):
                        player = self.state._get_player_from_id(player_id)

                        if player:
                            player.points += reward

            if self.state.round > MAX_ROUNDS or any(
                [p >= 50 for p in self.state.get_player_points()]
            ):
                self.state.finalise_game()
