from lib.interface.events.base_event import BaseEvent
from lib.interact.tile import Tile

from typing import Literal


class EventTilePlaced(BaseEvent):
    event_type: Literal["event_tile_placed"] = "event_tile_placed"
    player_id: int
    tile_placed: Tile
    placed_on: Tile
    placed_dir: Tile
