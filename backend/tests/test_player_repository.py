import pytest
import sample_data as data

from app.db.player_repository import get_player_by_id, player_exists
from tests.db_test_utils import create_test_player

pytestmark = pytest.mark.usefixtures("clear_test_database")


def test_get_player_by_id_returns_created_player() -> None:
    create_test_player()

    player = get_player_by_id(data.TEST_PLAYER_ID_1)

    assert player is not None

    assert player.player_id == data.TEST_PLAYER_ID_1
    assert player.display_name == data.TEST_DISPLAY_NAME_1


def test_get_player_by_id_returns_none_for_unknown_player() -> None:
    assert get_player_by_id("-1") is None


def test_player_exists_returns_true_for_existing_player() -> None:
    create_test_player()

    assert player_exists(data.TEST_PLAYER_ID_1)


def test_player_exists_returns_false_for_unknown_player() -> None:
    assert player_exists(data.TEST_PLAYER_ID_1) is False
