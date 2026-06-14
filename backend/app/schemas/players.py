from datetime import datetime

from pydantic import BaseModel, Field


class PlayerCreate(BaseModel):
    player_id: str = Field(min_length=1)
    display_name: str = Field(min_length=1)


class PlayerRead(PlayerCreate):
    created_at: datetime
