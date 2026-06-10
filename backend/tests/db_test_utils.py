from app.db.connection import get_connection


def clear_database_tables() -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM telemetry_events")
        conn.execute("DELETE FROM players")
        conn.execute("DELETE FROM matches")