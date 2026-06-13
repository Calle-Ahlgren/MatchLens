from app.db.connection import get_connection
from app.db.player_repository import create_player
from tests.db_test_utils import clear_database_tables

def test_create_player_inserts_player_row() -> None:
    clear_database_tables()
    create_player("player_test", "display_name_test")

    with get_connection() as conn:
        player_query = """
            SELECT player_id, display_name
            FROM players
            WHERE player_id = %s        
        """
        player_id = ("player_test",)

        cursor = conn.execute(player_query, player_id)
        result = cursor.fetchone()

        assert result is not None

        assert result[0] == "player_test"
        assert result[1] == "display_name_test"