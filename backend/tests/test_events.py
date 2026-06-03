import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.services.event_store import clear_events


client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_event_store() -> None:
    clear_events()
    pass


def test_create_event_accepts_valid_event() -> None:
    event = {
        "match_id": "match_001",
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle",
        }
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
        }
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
        }
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
        }
    }
    response = client.post("/events", json=event)

    assert response.status_code == 422

def test_list_events_returns_created_events() -> None:
    event = {
        "match_id": "match_001",
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle",
        }
    }

    response = client.post("/events", json=event)
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
    event = {
        "match_id": "match_001",
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle",
        }
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
    event = {
        "match_id": "match_001",
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle",
        }
    }

    client.post("/events", json=event)

    response = client.get("/events/not_an_id")

    assert response.status_code == 404
    assert response.json()["detail"] ==  "Event not found"