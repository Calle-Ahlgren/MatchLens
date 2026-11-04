import pytest
import sample_data as data

from app.db.match_repository import (
    create_match,
    get_match_by_id,
    list_matches,
    match_exists,
)
from app.schemas.matches import MatchCreate
from tests.db_test_utils import create_test_match

pytestmark = pytest.mark.usefixtures("clear_test_database")


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

    assert matches[0].started_at == data.TEST_MATCH_TIMESTAMP_LATE
    assert matches[1].started_at == data.TEST_MATCH_TIMESTAMP_EARLY


def test_match_exists_returns_true_for_existing_match() -> None:
    create_test_match()

    assert match_exists(data.TEST_MATCH_ID_1)


def test_match_exists_returns_false_for_unknown_match() -> None:
    assert match_exists(data.TEST_MATCH_ID_1) is False
