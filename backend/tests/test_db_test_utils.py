from datetime import UTC, datetime

from app.db.connection import get_connection
from tests.db_test_utils import clear_database_tables


def test_clear_database_tables_removes_match_rows() -> None:
    with get_connection() as conn:
        match_insert = """
            INSERT INTO matches (
                match_id,
                started_at,
                map_name,
                game_mode
            )
            VALUES (%s, %s, %s, %s)
        """
        match_values = (
            "match_repo_test",
            datetime.now(UTC),
            "map_repo_test",
            "mode_repo_test",
        )
        conn.execute(match_insert, match_values)
        
    clear_database_tables()

    with get_connection() as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM matches")
        count = cursor.fetchone()
        assert count is not None
        assert count[0] == 0