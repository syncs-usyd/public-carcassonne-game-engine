from pydantic import BaseModel


class PublicPlayerModel(BaseModel):
    player_id: int
    points: int
