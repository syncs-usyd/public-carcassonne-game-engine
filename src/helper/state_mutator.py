from helper.client_state import ClientSate

from lib.interact.tile import Tile
from lib.interface.events.event_player_bannned import EventPlayerBanned
from lib.interface.events.event_player_turn_started import EventPlayerTurnStarted
from lib.interface.events.event_player_won import EventPlayerWon
from lib.interface.events.event_river_phase_completed import EventRiverPhaseCompleted
from lib.interface.events.event_game_ended import (
    EventGameEndedCancelled,
    EventGameEndedPointLimitReaced,
    EventGameEndedStaleMate,
)
from lib.interface.events.event_game_started import (
    EventGameStarted,
    PublicEventGameStarted,
)
from lib.interface.events.event_player_drew_cards import (
    EventPlayerDrewCards,
    PublicEventPlayerDrewCards,
)
from lib.interface.events.event_player_meeple_freed import EventPlayerMeepleFreed
from lib.interface.events.event_tile_placed import (
    EventStartingTilePlaced,
)
from lib.interface.events.moves.move_place_meeple import (
    MovePlaceMeeple,
    MovePlaceMeeplePass,
)
from lib.interface.events.moves.move_place_tile import MovePlaceTile
from lib.interface.events.typing import EventType


class StateMutator:
    def __init__(self, state: ClientSate):
        self.state = state

    def commit(self, i: int, event: EventType):
        if i != len(self.state.event_history):
            raise RuntimeError("Please send us a discord message with this error log.")
        self.state.event_history.append(event)

        match event:
            case EventGameStarted() as e:
                self._commit_event_game_started(e)

            case PublicEventGameStarted() as e:
                self._commit_public_event_game_started(e)

            case EventPlayerDrewCards() as e:
                self._commit_player_drew_cards(e)

            case EventPlayerMeepleFreed() as e:
                self._commit_event_player_meeple_freed(e)

            case EventStartingTilePlaced() as e:
                self._commit_event_starting_tile_placed(e)

            case MovePlaceTile() as e:
                self._commit_move_place_tile(e)

            case MovePlaceMeeple() as e:
                self._commit_move_place_meeple(e)

            case MovePlaceMeeplePass() as e:
                self._commit_move_place_meeple_pass(e)

            case PublicEventPlayerDrewCards() as e:
                self._commit_opponent_drew_cards(e)

            case EventGameEndedPointLimitReaced() as e:
                self._commit_event_game_ended_point_limit(e)

            case EventGameEndedStaleMate() as e:
                self._commit_event_game_ended_stalemate(e)

            case EventGameEndedCancelled() as e:
                self._commit_event_game_ended_cancelled(e)

            case EventPlayerBanned() as e:
                self._commit_event_player_banned(e)

            case EventPlayerTurnStarted() as e:
                self._commit_event_player_turn_started(e)

            case EventPlayerWon() as e:
                self._commit_event_player_won(e)

            case EventRiverPhaseCompleted() as e:
                self._commit_event_river_phase_completed(e)

            case _:
                raise RuntimeError(f"Unrecognised event: {event}")

    def _commit_player_drew_cards(self, e: EventPlayerDrewCards) -> None:
        if e.player_id != self.state.me.player_id:
            raise RuntimeError("Please send us a discord message with this error log.")

        print("Log I drew cards")
        self.state.me.tiles.extend(e.cards)
        for card_model in e.cards:
            for card in self.state.map.available_tiles:
                if card_model.tile_type == card.tile_type:
                    self.state.my_cards.append(card)
                    self.state.map.available_tiles.remove(card)

    def _commit_opponent_drew_cards(self, e: PublicEventPlayerDrewCards) -> None:
        if e.player_id == self.state.me.player_id:
            raise RuntimeError("Please send us a discord message with this error log.")

        self.state.players[e.player_id].num_tiles += e.num_cards

    def _commit_event_game_started(self, e: EventGameStarted) -> None:
        raise RuntimeError("Please send us a discord message with this error log.")

    def _commit_public_event_game_started(self, e: PublicEventGameStarted) -> None:
        self.state.me = e.you
        self.state.turn_order = e.turn_order
        self.state.players = {p.player_id: p for p in e.players}

        self.state.map.start_river_phase()

    def _commit_event_player_meeple_freed(self, e: EventPlayerMeepleFreed) -> None:
        pass

    def _commit_event_starting_tile_placed(self, e: EventStartingTilePlaced) -> None:
        x, y = e.tile_placed.pos
        Tile.get_starting_tile().placed_pos = (x, y)
        self.state.map._grid[y][x] = Tile.get_starting_tile()
        self.state.map.placed_tiles.append(Tile.get_starting_tile())

    def _commit_move_place_tile(self, e: MovePlaceTile) -> None:
        pass

    def _commit_move_place_meeple(self, e: MovePlaceMeeple) -> None:
        pass

    def _commit_move_place_meeple_pass(self, e: MovePlaceMeeplePass) -> None:
        pass

    def _commit_event_game_ended_point_limit(
        self, e: EventGameEndedPointLimitReaced
    ) -> None:
        pass

    def _commit_event_game_ended_stalemate(self, e: EventGameEndedStaleMate) -> None:
        pass

    def _commit_event_game_ended_cancelled(self, e: EventGameEndedCancelled) -> None:
        pass

    def _commit_event_meeple_placed(self, e: EventMeeplePlaced) -> None:
        pass

    def _commit_event_player_banned(self, e: EventPlayerBanned) -> None:
        pass

    def _commit_event_player_turn_started(self, e: EventPlayerTurnStarted) -> None:
        pass

    def _commit_event_player_won(self, e: EventPlayerWon) -> None:
        pass

    def _commit_event_river_phase_completed(self, e: EventRiverPhaseCompleted) -> None:
        pass
