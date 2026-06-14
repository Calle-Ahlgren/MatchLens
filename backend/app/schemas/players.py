from datetime import datetime

from pydantic import BaseModel, Field


class PlayerCreate(BaseModel):
    player_id: str = Field(min_length=1)
    display_name: str = Field(min_length=1)


class PlayerRead(PlayerCreate):
    # TODO:
    # For now, PlayerRead can be identical to PlayerRead.
    # Later we may add ended_at or computed summary fields.
    pass
