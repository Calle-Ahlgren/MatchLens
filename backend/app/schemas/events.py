from typing import Any

from pydantic import BaseModel, Field


class TelemetryEventCreate(BaseModel):
    match_id: str = Field(min_length=1)
    event_type: str = Field(min_length=1)
    player_id: str | None = None
    timestamp: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)