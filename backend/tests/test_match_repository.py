import pytest

from app.db.connection import get_connection
from app.db.match_repository import create_match, get_match_by_id, list_matches
from app.schemas.matches import MatchCreate
from tests.db_test_utils import clear_database_tables, create_test_match
import sample_data as data


@pytest.fixture(autouse=True)
def clear_test_database() -> None:
    clear_database_tables()

    yield

    clear_database_tables()


def test_create_match_inserts_match_row() -> None:
    create_test_match()

    with get_connection() as conn:
        match_query = """
            SELECT match_id, map_name, game_mode
            FROM matches
            WHERE match_id = %s
        """
        match_id = (data.TEST_MATCH_ID_1,)
        cursor = conn.execute(match_query, match_id)
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == data.TEST_MATCH_ID_1
        assert result[1] == data.TEST_MAP
        assert result[2] == data.TEST_MODE


def test_get_match_by_id_returns_created_match() -> None:
    create_test_match()

    match = get_match_by_id(data.TEST_MATCH_ID_1)

    assert match is not None

    assert match.match_id == data.TEST_MATCH_ID_1
    assert match.started_at == data.TEST_MATCH_TIMESTAMP_EARLY
    assert match.map_name == data.TEST_MAP
    assert match.game_mode == data.TEST_MODE


def test_get_match_by_id_returns_none_for_unknown_match() -> None:
    assert get_match_by_id("-1") is None


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

    matches = list_matches()

    assert len(matches) == 2

    assert matches[0].started_at == data.TEST_MATCH_TIMESTAMP_EARLY
    assert matches[1].started_at == data.TEST_MATCH_TIMESTAMP_LATE
