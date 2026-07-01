import pytest
from fastapi.testclient import TestClient

from app.main import app
from tests.db_test_utils import (
    clear_database_tables,
    create_test_match,
    create_test_player,
)


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_test_state() -> None:
    clear_database_tables()

    yield

    clear_database_tables()


def create_required_event_parents() -> None:
    create_test_match()
    create_test_player()


def assert_validation_error_mentions(response, expected_text: str) -> None:
    assert response.status_code == 422

    messages = [error["msg"] for error in response.json()["detail"]]

    assert any(expected_text in message for message in messages), messages


def test_create_event_accepts_valid_event() -> None:
    create_required_event_parents()

    event = {
        "match_id": "match_001",
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle",
        },
    }

    response = client.post("/events", json=event)

    response_json = response.json()

    assert response.status_code == 200
    assert response_json["event_id"]
    assert response_json["match_id"] == event["match_id"]
    assert response_json["event_type"] == event["event_type"]
    assert response_json["player_id"] == event["player_id"]
    assert response_json["timestamp"] == event["timestamp"]
    assert response_json["payload"] == event["payload"]


def test_create_event_rejects_missing_match_id() -> None:
    event = {
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle",
        },
    }

    response = client.post("/events", json=event)

    assert response.status_code == 422
    assert "match_id" in str(response.json())


def test_create_event_rejects_unknown_event_type() -> None:
    event = {
        "match_id": "match_001",
        "event_type": "shotfired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle",
        },
    }

    response = client.post("/events", json=event)

    assert response.status_code == 422


def test_create_event_rejects_invalid_timestamp() -> None:
    event = {
        "match_id": "match_001",
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-0a-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle",
        },
    }
    response = client.post("/events", json=event)

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("event_type", "payload", "expected_field"),
    [
        (
            "player_spawned",
            {"y": 0},
            "'x'",
        ),
        (
            "player_spawned",
            {"x": 0},
            "'y'",
        ),
        (
            "position_updated",
            {"y": 0},
            "'x'",
        ),
        (
            "position_updated",
            {"x": 0},
            "'y'",
        ),
        (
            "shot_fired",
            {},
            "'weapon'",
        ),
        (
            "player_hit",
            {
                "damage": 34,
                "weapon": "rifle",
            },
            "'target_player_id'",
        ),
        (
            "player_hit",
            {
                "target_player_id": "player_002",
                "weapon": "rifle",
            },
            "'damage'",
        ),
        (
            "player_hit",
            {
                "target_player_id": "player_002",
                "damage": 34,
            },
            "'weapon'",
        ),
        (
            "player_killed",
            {
                "weapon": "rifle",
            },
            "'victim_player_id'",
        ),
        (
            "player_killed",
            {
                "victim_player_id": "player_002",
            },
            "'weapon'",
        ),
        (
            "player_death",
            {
                "weapon": "rifle",
                "x": 0,
                "y": 0,
            },
            "'killer_player_id'",
        ),
        (
            "player_death",
            {
                "killer_player_id": "player_002",
                "x": 0,
                "y": 0,
            },
            "'weapon'",
        ),
        (
            "player_death",
            {
                "killer_player_id": "player_002",
                "weapon": "rifle",
                "y": 0,
            },
            "'x'",
        ),
        (
            "player_death",
            {
                "killer_player_id": "player_002",
                "weapon": "rifle",
                "x": 0,
            },
            "'y'",
        ),
    ],
)
def test_create_event_rejects_missing_required_payload_fields(
    event_type: str,
    payload: dict[str, object],
    expected_field: str,
) -> None:
    create_required_event_parents()

    event = {
        "match_id": "match_001",
        "event_type": event_type,
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": payload,
    }

    response = client.post("/events", json=event)

    assert_validation_error_mentions(response, expected_field)


@pytest.mark.parametrize(
    ("event_type", "payload", "expected_field"),
    [
        (
            "shot_fired",
            {
                "weapon": 123,
            },
            "'weapon'",
        ),
        (
            "player_hit",
            {
                "target_player_id": 123,
                "damage": 34,
                "weapon": "rifle",
            },
            "'target_player_id'",
        ),
        (
            "player_hit",
            {
                "target_player_id": "player_002",
                "damage": 34,
                "weapon": 123,
            },
            "'weapon'",
        ),
        (
            "player_killed",
            {
                "victim_player_id": 123,
                "weapon": "rifle",
            },
            "'victim_player_id'",
        ),
        (
            "player_killed",
            {
                "victim_player_id": "player_002",
                "weapon": 123,
            },
            "'weapon'",
        ),
        (
            "player_death",
            {
                "killer_player_id": 123,
                "weapon": "rifle",
                "x": 10,
                "y": 20,
            },
            "'killer_player_id'",
        ),
        (
            "player_death",
            {
                "killer_player_id": "player_002",
                "weapon": 123,
                "x": 10,
                "y": 20,
            },
            "'weapon'",
        ),
    ],
)
def test_create_event_rejects_string_payload_fields_with_wrong_type(
    event_type: str,
    payload: dict[str, object],
    expected_field: str,
) -> None:
    create_required_event_parents()

    event = {
        "match_id": "match_001",
        "event_type": event_type,
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": payload,
    }

    response = client.post("/events", json=event)

    assert_validation_error_mentions(response, expected_field)


@pytest.mark.parametrize(
    ("event_type", "payload", "expected_field"),
    [
        (
            "player_spawned",
            {
                "x": "left",
                "y": 20,
            },
            "'x'",
        ),
        (
            "player_spawned",
            {
                "x": 10,
                "y": "up",
            },
            "'y'",
        ),
        (
            "position_updated",
            {
                "x": "left",
                "y": 20,
            },
            "'x'",
        ),
        (
            "position_updated",
            {
                "x": 10,
                "y": "up",
            },
            "'y'",
        ),
        (
            "player_hit",
            {
                "target_player_id": "player_002",
                "damage": "a lot",
                "weapon": "rifle",
            },
            "'damage'",
        ),
        (
            "player_death",
            {
                "killer_player_id": "player_002",
                "weapon": "rifle",
                "x": "left",
                "y": 20,
            },
            "'x'",
        ),
        (
            "player_death",
            {
                "killer_player_id": "player_002",
                "weapon": "rifle",
                "x": 10,
                "y": "up",
            },
            "'y'",
        ),
    ],
)
def test_create_event_rejects_numeric_payload_fields_with_string_values(
    event_type: str,
    payload: dict[str, object],
    expected_field: str,
) -> None:
    create_required_event_parents()

    event = {
        "match_id": "match_001",
        "event_type": event_type,
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": payload,
    }

    response = client.post("/events", json=event)

    assert_validation_error_mentions(response, expected_field)


@pytest.mark.parametrize(
    ("event_type", "payload", "expected_field"),
    [
        (
            "player_spawned",
            {
                "x": True,
                "y": 20,
            },
            "'x'",
        ),
        (
            "player_spawned",
            {
                "x": 10,
                "y": False,
            },
            "'y'",
        ),
        (
            "position_updated",
            {
                "x": True,
                "y": 20,
            },
            "'x'",
        ),
        (
            "position_updated",
            {
                "x": 10,
                "y": False,
            },
            "'y'",
        ),
        (
            "player_hit",
            {
                "target_player_id": "player_002",
                "damage": True,
                "weapon": "rifle",
            },
            "'damage'",
        ),
        (
            "player_death",
            {
                "killer_player_id": "player_002",
                "weapon": "rifle",
                "x": True,
                "y": 20,
            },
            "'x'",
        ),
        (
            "player_death",
            {
                "killer_player_id": "player_002",
                "weapon": "rifle",
                "x": 10,
                "y": False,
            },
            "'y'",
        ),
    ],
)
def test_create_event_rejects_numeric_payload_fields_with_boolean_values(
    event_type: str,
    payload: dict[str, object],
    expected_field: str,
) -> None:
    create_required_event_parents()

    event = {
        "match_id": "match_001",
        "event_type": event_type,
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": payload,
    }

    response = client.post("/events", json=event)

    assert_validation_error_mentions(response, expected_field)


def test_list_events_returns_created_events() -> None:
    create_required_event_parents()

    event = {
        "match_id": "match_001",
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle",
        },
    }

    client.post("/events", json=event)
    events = client.get("/events")

    assert events.status_code == 200

    events_json = events.json()

    assert len(events_json) == 1
    assert events_json[0]["match_id"] == event["match_id"]
    assert events_json[0]["event_type"] == event["event_type"]
    assert events_json[0]["player_id"] == event["player_id"]
    assert events_json[0]["timestamp"] == event["timestamp"]
    assert events_json[0]["payload"] == event["payload"]
    assert events_json[0]["event_id"]


def test_get_event_by_id_returns_created_event() -> None:
    create_required_event_parents()

    event = {
        "match_id": "match_001",
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle",
        },
    }

    post_response = client.post("/events", json=event)
    post_event = post_response.json()
    event_id = post_event["event_id"]

    get_response = client.get(f"/events/{event_id}")

    assert get_response.status_code == 200
    get_event = get_response.json()

    assert get_event["event_id"] == event_id
    assert get_event["match_id"] == event["match_id"]
    assert get_event["event_type"] == event["event_type"]
    assert get_event["player_id"] == event["player_id"]
    assert get_event["timestamp"] == event["timestamp"]
    assert get_event["payload"] == event["payload"]


def test_get_event_by_id_returns_404_for_unknown_event() -> None:
    response = client.get("/events/not_an_id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"
