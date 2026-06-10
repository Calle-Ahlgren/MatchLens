# Database repository functions for matches.
# These are not wired into the API yet.

from datetime import datetime

from app.db.connection import get_connection


def create_match(match_id: str, started_at: datetime, map_name: str, game_mode: str) -> None:
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
        match_values = (match_id, started_at, map_name, game_mode)
        conn.execute(match_insert, match_values)