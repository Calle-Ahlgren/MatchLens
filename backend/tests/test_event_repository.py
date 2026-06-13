from datetime import UTC, datetime

from app.db.connection import get_connection
from app.db.event_repository import create_event, get_event_by_id, list_events
from app.db.match_repository import create_match
from app.db.player_repository import create_player
from app.schemas.events import EventType, TelemetryEventCreate, TelemetryEventRead
from tests.db_test_utils import clear_database_tables

match_test_id = "match_test"
timestamp_test = datetime(2026, 1, 1, 1, 1, 1, tzinfo=UTC)
player_test_id = "player_test"
payload_test = {
        "weapon": "rifle",
        "damage": 34,
    }

def create_test_match() -> None:
    create_match(match_test_id, timestamp_test, "map_test", "mode_test")

def create_test_player() -> None:
    create_player(player_test_id, "display_name_test")

def create_test_event() -> TelemetryEventRead:
    clear_database_tables()
    create_test_match()
    create_test_player()

    event = TelemetryEventCreate(
        match_id=match_test_id,
        event_type=EventType.SHOT_FIRED,
        player_id=player_test_id,
        timestamp=timestamp_test,
        payload=payload_test
    )

    return create_event(event)

def test_create_event_inserts_telemetry_event_row() -> None:    
    event = create_test_event()

    with get_connection() as conn:
        query = """
            SELECT match_id, player_id, event_type, payload
            FROM telemetry_events
            WHERE event_id = %s
        """
        cursor = conn.execute(query, (event.event_id,))
        result = cursor.fetchone()

        assert result is not None
        assert result[0] == event.match_id
        assert result[1] == event.player_id
        assert result[2] == event.event_type.value
        assert result[3] == event.payload

def test_get_event_by_id_returns_created_event() -> None:
    created_event = create_test_event()

    returned_event = get_event_by_id(created_event.event_id)

    assert returned_event is not None
    assert returned_event.event_id == created_event.event_id
    assert returned_event.match_id == created_event.match_id
    assert returned_event.player_id == created_event.player_id
    assert returned_event.event_type == created_event.event_type
    assert returned_event.timestamp == created_event.timestamp
    assert returned_event.payload == created_event.payload


def test_get_event_by_id_returns_none_for_unknown_event() -> None:
    clear_database_tables()
    assert get_event_by_id("-1") is None

def test_list_events_returns_created_events_in_time_order() -> None:
    clear_database_tables()
    create_test_match()
    create_test_player()

    timestamp_later = datetime(2026, 1, 1, 1, 2, 1, tzinfo=UTC)

    event1 = TelemetryEventCreate(
        match_id=match_test_id,
        event_type=EventType.SHOT_FIRED,
        player_id=player_test_id,
        timestamp=timestamp_later,
        payload=payload_test,
    )

    event2 = TelemetryEventCreate(
        match_id=match_test_id,
        event_type=EventType.PLAYER_SPAWNED,
        player_id=player_test_id,
        timestamp=timestamp_test,
        payload={
            "x": 0,
            "y": 1,
            "z": 0
        },
    )

    create_event(event1)
    create_event(event2)

    events = list_events()

    assert len(events) == 2

    assert events[0].timestamp == timestamp_test
    assert events[1].timestamp == timestamp_later