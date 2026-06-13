from datetime import UTC, datetime

from app.db.connection import get_connection
from app.db.event_repository import create_event
from app.db.match_repository import create_match
from app.db.player_repository import create_player
from app.schemas.events import EventType, TelemetryEventCreate
from tests.db_test_utils import clear_database_tables


def test_create_event_inserts_telemetry_event_row() -> None:
    clear_database_tables()
    match_test_id = "match_test"
    timestamp_test = datetime(2026, 1, 1, 1, 1, 1, tzinfo=UTC)
    player_test_id = "player_test"
    payload_test = {
            "weapon": "rifle",
            "damage": 34,
        }

    create_match(match_test_id, timestamp_test, "map_test", "mode_test")
    create_player(player_test_id, "display_name_test")

    event = TelemetryEventCreate(
        match_id=match_test_id,
        event_type=EventType.SHOT_FIRED,
        player_id=player_test_id,
        timestamp=timestamp_test,
        payload=payload_test
    )

    event_read = create_event(event)

    with get_connection() as conn:
        query = """
            SELECT match_id, player_id, event_type, payload
            FROM telemetry_events
            WHERE event_id = %s
        """
        cursor = conn.execute(query, (event_read.event_id,))
        result = cursor.fetchone()

        assert result is not None
        assert result[0] == match_test_id
        assert result[1] == player_test_id
        assert result[2] == EventType.SHOT_FIRED.value
        assert result[3] == payload_test