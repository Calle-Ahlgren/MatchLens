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


PLAYER_OWNED_EVENT_TYPES = {
    EventType.PLAYER_SPAWNED,
    EventType.POSITION_UPDATED,
    EventType.SHOT_FIRED,
    EventType.PLAYER_HIT,
    EventType.PLAYER_KILLED,
    EventType.PLAYER_DEATH,
}


REQUIRED_PAYLOAD_FIELDS_AND_TYPES: dict[
    EventType, dict[str, type | tuple[type, ...]]
] = {
    EventType.PLAYER_SPAWNED: {
        "x": (int, float),
        "y": (int, float),
    },
    EventType.POSITION_UPDATED: {
        "x": (int, float),
        "y": (int, float),
    },
    EventType.SHOT_FIRED: {
        "weapon": str,
    },
    EventType.PLAYER_HIT: {
        "target_player_id": str,
        "damage": (int, float),
        "weapon": str,
    },
    EventType.PLAYER_KILLED: {
        "victim_player_id": str,
        "weapon": str,
    },
    EventType.PLAYER_DEATH: {
        "killer_player_id": str,
        "weapon": str,
        "x": (int, float),
        "y": (int, float),
    },
}


class TelemetryEventCreate(BaseModel):
    match_id: str = Field(min_length=1)
    event_type: EventType
    player_id: str | None = None
    timestamp: datetime
    payload: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_event_contract(self) -> "TelemetryEventCreate":
        if self.event_type in PLAYER_OWNED_EVENT_TYPES and self.player_id is None:
            raise ValueError("player_id is required for this event type")

        field_types = REQUIRED_PAYLOAD_FIELDS_AND_TYPES.get(self.event_type, {})

        required_fields = set(field_types.keys())
        payload_fields = set(self.payload.keys())

        missing_fields = required_fields - payload_fields

        if missing_fields:
            raise ValueError(
                f"Missing required payload fields: {sorted(missing_fields)}"
            )

        for field_name, expected_type in field_types.items():
            value = self.payload[field_name]

            if expected_type == (int, float):
                is_valid = isinstance(value, (int, float)) and not isinstance(
                    value, bool
                )
            else:
                is_valid = isinstance(value, expected_type)

            if not is_valid:
                raise ValueError(f"Invalid payload field '{field_name}': wrong type")

        return self


class TelemetryEventRead(TelemetryEventCreate):
    event_id: str = Field(min_length=1)
