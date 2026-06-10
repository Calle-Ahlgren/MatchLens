from datetime import UTC, datetime

from app.db.connection import get_connection
from app.db.match_repository import create_match
from tests.db_test_utils import clear_database_tables


def test_create_match_inserts_match_row() -> None:
    clear_database_tables()
    create_match("match_test", datetime.now(UTC), "map_test", "mode_test")

    with get_connection() as conn:
        match_query = """
            SELECT match_id, map_name, game_mode
            FROM matches
            WHERE match_id = %s
        """
        match_id = ("match_test",)
        cursor = conn.execute(match_query, match_id)
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == "match_test"
        assert result[1] == "map_test"
        assert result[2] == "mode_test"