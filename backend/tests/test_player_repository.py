import pytest

from app.db.connection import get_connection
from app.db.player_repository import get_player_by_id
from tests.db_test_utils import clear_database_tables, create_test_player
import sample_data as data


TEST_PLAYER_ID = "player_test"
TEST_DISPLAY_NAME = "display_name_test"


@pytest.fixture(autouse=True)
def clear_test_database() -> None:
    clear_database_tables()

    yield

    clear_database_tables()


def test_create_player_inserts_player_row() -> None:
    create_test_player()

    with get_connection() as conn:
        player_query = """
            SELECT player_id, display_name
            FROM players
            WHERE player_id = %s        
        """

        cursor = conn.execute(player_query, (data.TEST_PLAYER_ID_1,))
        result = cursor.fetchone()

        assert result is not None

        assert result[0] == data.TEST_PLAYER_ID_1
        assert result[1] == data.TEST_DISPLAY_NAME


def test_get_player_by_id_returns_created_player() -> None:
    create_test_player()

    player = get_player_by_id(data.TEST_PLAYER_ID_1)

    assert player is not None

    assert player.player_id == data.TEST_PLAYER_ID_1
    assert player.display_name == data.TEST_DISPLAY_NAME


def test_get_player_by_id_returns_none_for_unknown_player() -> None:
    assert get_player_by_id("-1") is None