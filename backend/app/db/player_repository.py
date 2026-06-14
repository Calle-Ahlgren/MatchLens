from app.db.connection import get_connection


def create_player(player_id: str, display_name: str) -> None:
    with get_connection() as conn:
        player_insert = """
            INSERT INTO players(
                player_id,
                display_name
            )
            VALUES (%s, %s)
        """

        player_values = (player_id, display_name)

        conn.execute(player_insert, player_values)
