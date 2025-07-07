from pydantic import BaseModel


class TileModel(BaseModel):
    player_tile_index: int
    tile_type: str
    rotatation: int
