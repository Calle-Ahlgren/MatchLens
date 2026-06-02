from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_event_accepts_valid_event() -> None:
    test_event = {
        "match_id": "match_001",
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle"
        }
    }

    response = client.post("/events", json=test_event)

    assert response.status_code == 200

    assert response.json() == test_event


def test_create_event_rejects_missing_match_id() -> None:
    test_event = {
        "event_type": "shot_fired",
        "player_id": "player_001",
        "timestamp": "2026-06-02T18:30:00Z",
        "payload": {
            "damage": 34,
            "weapon": "rifle"
        }
    }

    response = client.post("/events", json=test_event)

    assert response.status_code == 422
    assert "match_id" in str(response.json())