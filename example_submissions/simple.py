#### DISCLAIMER ####
# This was produced with the assistance of GPT 4o

from helper.game import Game
from lib.interface.events.moves.move_place_meeple import (
    MovePlaceMeeple,
    MovePlaceMeeplePass,
)
from lib.interface.events.moves.move_place_tile import MovePlaceTile
from lib.interface.queries.typing import QueryType
from lib.interface.queries.query_place_tile import QueryPlaceTile
from lib.interface.queries.query_place_meeple import QueryPlaceMeeple
from lib.interface.events.moves.typing import MoveType
from lib.models.tile_model import TileModel


class BotState:
    def __init__(self):
        self.last_tile: TileModel | None = None


def main():
    game = Game()
    bot_state = BotState()

    while True:
        query = game.get_next_query()

        def choose_move(query: QueryType) -> MoveType:
            match query:
                case QueryPlaceTile() as q:
                    return handle_place_tile(game, bot_state, q)

                case QueryPlaceMeeple() as q:
                    return handle_place_meeple(game, bot_state, q)

        game.send_move(choose_move(query))


def handle_place_tile(
    game: Game, bot_state: BotState, query: QueryPlaceTile
) -> MovePlaceTile:
    """Randomly place a tile from the options available."""
    # Naively choose the first tile
    tile_index = 0
    tile = game.state.me.tiles[tile_index]
    bot_state.last_tile = tile  # Remember for next phase
    return game.move_place_tile(query, tile, tile_index)


def handle_place_meeple(
    game: Game, bot_state: BotState, query: QueryPlaceMeeple
) -> MovePlaceMeeple | MovePlaceMeeplePass:
    """Try to place a meeple on the tile just placed, or pass."""
    assert bot_state.last_tile is not None
    structures = game.state.get_tile_structures(bot_state.last_tile)
    bot_state.last_tile = None
    if structures:
        return game.move_place_meeple(
            query, bot_state.last_tile, placed_on=next(iter(structures))
        )
    else:
        return game.move_place_meeple_pass(query)


if __name__ == "__main__":
    main()
