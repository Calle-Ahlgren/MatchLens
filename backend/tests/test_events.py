import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.events import EventType
from tests.db_test_utils import (
    create_test_match,
    create_test_player,
)

pytestmark = pytest.mark.usefixtures("clear_test_database")

client = TestClient(app)


def create_required_event_parents() -> None:
    create_test_match()
    create_test_player()


def assert_validation_error_mentions(response, expected_text: str) -> None:
    assert response.status_code == 422

    messages = [error["msg"] for error in response.json()["detail"]]

    assert any(expected_text in message for message in messages), messages


def valid_payload_for_event_type(event_type: str) -> dict[str, object]:
    payload = {}
    match event_type:
        case EventType.PLAYER_SPAWNED:
            payload = {"x": 0, "y": 0}
        case EventType.POSITION_UPDATED:
            payload = {"x": 10, "y": 20}
        case EventType.SHOT_FIRED:
            payload = {"weapon": "rifle"}
        case EventType.PLAYER_HIT:
            payload = {
                "target_player_id": "player_002",
                "damage": 34,
                "weapon": "rifle",
            }
        case EventType.PLAYER_KILLED:
            payload = {"victim_player_id": "player_002", "weapon": "rifle"}
        case EventType.PLAYER_DEATH:
            payload = {
                "killer_player_id": "player_002",
                "weapon": "rifle",
                "x": 0,
                "y": 0,
            }

    return payload


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


@pytest.mark.parametrize(
    "event_type",
    [
        "player_spawned",
        "position_updated",
        "shot_fired",
        "player_hit",
        "player_killed",
        "player_death",
    ],
)
def test_create_event_rejects_missing_player_id_for_player_owned_events(
    event_type: str,
) -> None:
    create_required_event_parents()

    event = {
        "match_id": "match_001",
        "event_type": event_type,
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": valid_payload_for_event_type(event_type),
    }

    response = client.post("/events", json=event)

    assert_validation_error_mentions(response, "player_id")


def test_create_event_returns_404_for_unknown_match() -> None:
    create_test_player()

    event = {
        "match_id": "nonexistant_match",
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle",
        },
    }

    response = client.post("/events", json=event)

    assert response.status_code == 404

    assert response.json()["detail"] == "Match not found"


def test_create_event_returns_404_for_unknown_player() -> None:
    create_test_match()

    event = {
        "match_id": "match_001",
        "event_type": "shot_fired",
        "player_id": "nonexistant_player",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle",
        },
    }

    response = client.post("/events", json=event)

    assert response.status_code == 404

    assert response.json()["detail"] == "Player not found"
