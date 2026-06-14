import pytest
from fastapi.testclient import TestClient

from app.db.match_repository import create_match
from app.main import app
from app.schemas.matches import MatchCreate
from tests.db_test_utils import clear_database_tables, create_test_match
import sample_data as data


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_test_database() -> None:
    clear_database_tables()

    yield

    clear_database_tables()


def test_get_match_by_id_returns_created_match() -> None:
    create_test_match()

    response = client.get(f"/matches/{data.TEST_MATCH_ID_1}")

    assert response.status_code == 200

    match = response.json()

    assert match["match_id"] == data.TEST_MATCH_ID_1
    assert match["started_at"] == "2026-01-01T01:01:01Z"
    assert match["map_name"] == data.TEST_MAP
    assert match["game_mode"] == data.TEST_MODE


def test_get_match_by_id_returns_404_for_unknown_match() -> None:
    response = client.get("/matches/not_a_match")

    assert response.status_code == 404

    assert response.json()["detail"] == "Match not found"


def test_create_match_accepts_valid_match() -> None:
    match = {
        "match_id": data.TEST_MATCH_ID_1,
        "started_at": "2026-01-01T01:01:01Z",
        "map_name": data.TEST_MAP,
        "game_mode": data.TEST_MODE,
    }

    response = client.post("/matches", json=match)
    response_json = response.json()

    assert response.status_code == 200

    assert response_json["match_id"] == data.TEST_MATCH_ID_1
    assert response_json["started_at"] == "2026-01-01T01:01:01Z"
    assert response_json["map_name"] == data.TEST_MAP
    assert response_json["game_mode"] == data.TEST_MODE


def test_create_match_rejects_empty_match_id() -> None:
    match = {
        "match_id": "",
        "started_at": "2026-01-01T01:01:01Z",
        "map_name": data.TEST_MAP,
        "game_mode": data.TEST_MODE,
    }

    response = client.post("/matches", json=match)

    assert response.status_code == 422


def test_list_matches_returns_created_matches_in_start_time_order() -> None:
    create_match(
        MatchCreate(
            match_id=data.TEST_MATCH_ID_2,
            started_at=data.TEST_MATCH_TIMESTAMP_LATE,
            map_name=data.TEST_MAP,
            game_mode=data.TEST_MODE,
        )
    )
    create_test_match()

    response = client.get("/matches")
    matches = response.json()

    assert response.status_code == 200
    assert len(matches) == 2

    assert matches[0]["match_id"] == data.TEST_MATCH_ID_1
    assert matches[0]["started_at"] == "2026-01-01T01:01:01Z"

    assert matches[1]["match_id"] == "match_002"
    assert matches[1]["started_at"] == "2026-01-01T02:01:01Z"
