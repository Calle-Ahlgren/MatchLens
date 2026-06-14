from datetime import UTC, datetime

import pytest

from app.db.connection import get_connection
from app.db.match_repository import create_match, get_match_by_id, list_matches
from tests.db_test_utils import clear_database_tables

TEST_MATCH_ID = "match_001"
TEST_MATCH_TIMESTAMP = datetime(2026, 1, 1, 1, 1, 1, tzinfo=UTC)
TEST_MAP = "map_001"
TEST_MODE = "mode_001"


@pytest.fixture(autouse=True)
def clear_test_database() -> None:
    clear_database_tables()

    yield

    clear_database_tables()


def create_test_match() -> None:
    create_match(TEST_MATCH_ID, TEST_MATCH_TIMESTAMP, TEST_MAP, TEST_MODE)


def test_create_match_inserts_match_row() -> None:
    create_test_match()

    with get_connection() as conn:
        match_query = """
            SELECT match_id, map_name, game_mode
            FROM matches
            WHERE match_id = %s
        """
        match_id = (TEST_MATCH_ID,)
        cursor = conn.execute(match_query, match_id)
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == TEST_MATCH_ID
        assert result[1] == TEST_MAP
        assert result[2] == TEST_MODE


def test_get_match_by_id_returns_created_match() -> None:
    create_test_match()

    match = get_match_by_id(TEST_MATCH_ID)

    assert match is not None

    assert match.match_id == TEST_MATCH_ID
    assert match.started_at == TEST_MATCH_TIMESTAMP
    assert match.map_name == TEST_MAP
    assert match.game_mode == TEST_MODE


def test_get_match_by_id_returns_none_for_unknown_match() -> None:
    assert get_match_by_id("-1") is None


def test_list_matches_returns_created_matches_in_start_time_order() -> None:
    timestamp_late = datetime(2026, 1, 1, 2, 1, 1, tzinfo=UTC)
    create_match("match_002", timestamp_late, TEST_MAP, TEST_MODE)
    create_test_match()

    matches = list_matches()

    assert len(matches) == 2

    assert matches[0].started_at == TEST_MATCH_TIMESTAMP
    assert matches[1].started_at == timestamp_late
