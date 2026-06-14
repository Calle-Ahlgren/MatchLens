from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from app.db.match_repository import create_match
from app.main import app
from tests.db_test_utils import clear_database_tables


client = TestClient(app)

TEST_MATCH_ID = "match_001"
TEST_MATCH_TIMESTAMP = datetime(2026, 1, 1, 1, 1, 1, tzinfo=UTC)
TEST_MAP = "map_001"
TEST_MODE = "mode_001"


@pytest.fixture(autouse=True)
def clear_test_database() -> None:
    clear_database_tables()

    yield

    clear_database_tables()


def test_get_match_by_id_returns_created_match() -> None:
    create_match(TEST_MATCH_ID, TEST_MATCH_TIMESTAMP, TEST_MAP, TEST_MODE)

    response = client.get(f"/matches/{TEST_MATCH_ID}")

    assert response.status_code == 200

    match = response.json()

    assert match["match_id"] == TEST_MATCH_ID
    assert match["started_at"] == "2026-01-01T01:01:01Z"
    assert match["map_name"] == TEST_MAP
    assert match["game_mode"] == TEST_MODE


def test_get_match_by_id_returns_404_for_unknown_match() -> None:
    response = client.get("/matches/not_a_match")

    assert response.status_code == 404

    assert response.json()["detail"] == "Match not found"


def test_create_match_accepts_valid_match() -> None:
    match = {
        "match_id": TEST_MATCH_ID,
        "started_at": "2026-01-01T01:01:01Z",
        "map_name": TEST_MAP,
        "game_mode": TEST_MODE,
    }

    response = client.post("/matches", json=match)
    response_json = response.json()

    assert response.status_code == 200

    assert response_json["match_id"] == TEST_MATCH_ID
    assert response_json["started_at"] == "2026-01-01T01:01:01Z"
    assert response_json["map_name"] == TEST_MAP
    assert response_json["game_mode"] == TEST_MODE


def test_create_match_rejects_empty_match_id() -> None:
    match = {
        "match_id": "",
        "started_at": "2026-01-01T01:01:01Z",
        "map_name": TEST_MAP,
        "game_mode": TEST_MODE,
    }

    response = client.post("/matches", json=match)

    assert response.status_code == 422