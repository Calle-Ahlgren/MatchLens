# Database repository functions for matches.
# These are not wired into the API yet.

from datetime import datetime

from app.db.connection import get_connection
from app.schemas.matches import MatchRead


def create_match(match_id: str, started_at: datetime, map_name: str, game_mode: str) -> None:
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
    
    with get_connection() as conn:
        conn.execute(match_insert, match_values)


def get_match_by_id(match_id: str) -> MatchRead | None:
    query = """
        SELECT match_id, started_at, map_name, game_mode
        FROM matches
        WHERE match_id = %s
    """

    with get_connection() as conn:
        result = conn.execute(query, (match_id,)).fetchone()

    if result is None:
        return None
    
    return MatchRead(
        match_id=result[0],
        started_at=result[1],
        map_name=result[2],
        game_mode=result[3],
    )