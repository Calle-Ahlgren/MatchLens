from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_event_accepts_valid_event() -> None:
    event = {
        "match_id": "match_001",
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle"
        }
    }

    response = client.post("/events", json=event)

    assert response.status_code == 200

    assert response.json() == event


def test_create_event_rejects_missing_match_id() -> None:
    event = {
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle"
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
            "weapon": "rifle"
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
            "weapon": "rifle"
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
            "weapon": "rifle"
        }
    }

    response = client.post("/events", json=event)
    events = client.get("/events")

    assert events.status_code == 200
    assert event in events.json()