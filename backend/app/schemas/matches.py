from datetime import datetime

from pydantic import BaseModel, Field


class MatchCreate(BaseModel):
    match_id: str = Field(min_length=1)
    started_at: datetime
    map_name: str = Field(min_length=1)
    game_mode: str = Field(min_length=1)


class MatchRead(MatchCreate):
    pass
