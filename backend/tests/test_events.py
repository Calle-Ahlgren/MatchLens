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

    events_json = events.json()

    assert any(
        stored_event["match_id"] == event["match_id"]
        and stored_event["event_type"] == event["event_type"]
        and stored_event["player_id"] == event["player_id"]
        and stored_event["timestamp"] == event["timestamp"]
        and stored_event["payload"] == event["payload"]
        and stored_event["event_id"]
        for stored_event in events_json
)