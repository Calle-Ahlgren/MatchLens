from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class EventType(StrEnum):
    MATCH_STARTED = "match_started"
    PLAYER_SPAWNED = "player_spawned"
    POSITION_UPDATED = "position_updated"
    SHOT_FIRED = "shot_fired"
    PLAYER_HIT = "player_hit"
    PLAYER_KILLED = "player_killed"
    MATCH_ENDED = "match_ended"


class TelemetryEventCreate(BaseModel):
    match_id: str = Field(min_length=1)
    event_type: EventType
    player_id: str | None = None
    timestamp: datetime
    payload: dict[str, Any] = Field(default_factory=dict)

class TelemetryEventRead(TelemetryEventCreate):
    event_id: str = Field(min_length=1)