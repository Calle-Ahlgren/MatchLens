from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, model_validator


class EventType(StrEnum):
    PLAYER_SPAWNED = "player_spawned"
    POSITION_UPDATED = "position_updated"
    SHOT_FIRED = "shot_fired"
    PLAYER_HIT = "player_hit"
    PLAYER_KILLED = "player_killed"
    PLAYER_DEATH = "player_death"


REQUIRED_PAYLOAD_FIELDS: dict[EventType, set[str]] = {
    EventType.PLAYER_SPAWNED: {"x", "y"},
    EventType.POSITION_UPDATED: {"x", "y"},
    EventType.SHOT_FIRED: {"weapon"},
    EventType.PLAYER_HIT: {"target_player_id", "damage", "weapon"},
    EventType.PLAYER_KILLED: {"victim_player_id", "weapon"},
    EventType.PLAYER_DEATH: {"killer_player_id", "weapon", "x", "y"},
}


class TelemetryEventCreate(BaseModel):
    match_id: str = Field(min_length=1)
    event_type: EventType
    player_id: str | None = None
    timestamp: datetime
    payload: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_payload_for_event_type(self) -> "TelemetryEventCreate":
        required_fields = REQUIRED_PAYLOAD_FIELDS.get(self.event_type, set())

        payload_fields = set(self.payload.keys())

        missing_fields = required_fields - payload_fields

        if missing_fields:
            raise ValueError(f"Missing required payload fields: {sorted(missing_fields)}")

        return self


class TelemetryEventRead(TelemetryEventCreate):
    event_id: str = Field(min_length=1)
