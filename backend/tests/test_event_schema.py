import pytest
from pydantic import ValidationError

from app.schemas.events import TelemetryEventCreate

INVALID_PAYLOAD_CASES = [
    # Missing required fields — one case for each event type
    pytest.param(
        "player_spawned",
        {"y": 0},
        "'x'",
        id="spawn-missing-x",
    ),
    pytest.param(
        "position_updated",
        {"x": 10},
        "'y'",
        id="position-missing-y",
    ),
    pytest.param(
        "shot_fired",
        {},
        "'weapon'",
        id="shot-missing-weapon",
    ),
    pytest.param(
        "player_hit",
        {"damage": 34, "weapon": "rifle"},
        "'target_player_id'",
        id="hit-missing-target",
    ),
    pytest.param(
        "player_killed",
        {"weapon": "rifle"},
        "'victim_player_id'",
        id="kill-missing-victim",
    ),
    pytest.param(
        "player_death",
        {"weapon": "rifle", "x": 0, "y": 0},
        "'killer_player_id'",
        id="death-missing-killer",
    ),
    # Incorrect string field type
    pytest.param(
        "shot_fired",
        {"weapon": 123},
        "'weapon'",
        id="shot-invalid-weapon-type",
    ),
    # Incorrect numeric field type
    pytest.param(
        "position_updated",
        {"x": "left", "y": 20},
        "'x'",
        id="position-invalid-x-type",
    ),
    # Boolean values must not be accepted as numbers
    pytest.param(
        "player_spawned",
        {"x": True, "y": 20},
        "'x'",
        id="spawn-boolean-x",
    ),
    pytest.param(
        "player_hit",
        {"target_player_id": "player_002", "damage": True, "weapon": "rifle"},
        "'damage'",
        id="hit-boolean-damage",
    ),
]


@pytest.mark.parametrize(
    ("event_type", "payload", "expected_field"),
    INVALID_PAYLOAD_CASES,
)
def test_event_schema_rejects_invalid_payload(
    event_type: str,
    payload: dict[str, object],
    expected_field: str,
) -> None:
    event_data = {
        "match_id": "match_001",
        "event_type": event_type,
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": payload,
    }

    with pytest.raises(ValidationError) as e_info:
        TelemetryEventCreate.model_validate(event_data)

    assert expected_field in str(e_info.value)
