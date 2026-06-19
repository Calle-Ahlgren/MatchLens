from app.db.connection import get_connection
from app.schemas.players import PlayerCreate, PlayerRead


def create_player(player: PlayerCreate) -> PlayerRead:
    player_insert = """
        INSERT INTO players(
            player_id,
            display_name
        )
        VALUES (%s, %s)
        RETURNING player_id, display_name, created_at
    """

    player_values = (player.player_id, player.display_name)

    with get_connection() as conn:
        result = conn.execute(player_insert, player_values).fetchone()

    return PlayerRead(
        player_id=result[0],
        display_name=result[1],
        created_at=result[2],
    )


def get_player_by_id(player_id: str) -> PlayerRead | None:
    query = """
        SELECT player_id, display_name, created_at
        FROM players
        WHERE player_id = %s
    """
    with get_connection() as conn:
        result = conn.execute(query, (player_id,)).fetchone()

    if result is None:
        return None

    return PlayerRead(
        player_id=result[0],
        display_name=result[1],
        created_at=result[2],
    )


def list_players() -> list[PlayerRead]:
    query = """
        SELECT player_id, display_name, created_at
        FROM players
        ORDER BY created_at
    """

    players = []

    with get_connection() as conn:
        rows = conn.execute(query).fetchall()

    for row in rows:
        players.append(
            PlayerRead(
                player_id=row[0],
                display_name=row[1],
                created_at=row[2],
            )
        )

    return players
