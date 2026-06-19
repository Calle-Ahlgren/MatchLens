import pytest

from app.db.connection import get_connection
from app.db.event_repository import (
    create_event, get_event_by_id, list_events, list_events_by_match_id, list_player_match_events
)
from app.db.match_repository import create_match
from app.db.player_repository import create_player
from app.schemas.events import EventType, TelemetryEventCreate
from app.schemas.matches import MatchCreate
from app.schemas.players import PlayerCreate
import sample_data as data
from tests.db_test_utils import (
    clear_database_tables, create_test_event, create_test_match, create_test_player,
)


@pytest.fixture(autouse=True)
def clear_test_state() -> None:
    clear_database_tables()

    yield

    clear_database_tables()


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
    assert get_event_by_id("-1") is None


def test_list_events_returns_created_events_in_time_order() -> None:
    create_test_match()
    create_test_player()

    event1 = TelemetryEventCreate(
        match_id=data.TEST_MATCH_ID_1,
        event_type=EventType.SHOT_FIRED,
        player_id=data.TEST_PLAYER_ID_1,
        timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
        payload=data.test_payload(),
    )

    event2 = TelemetryEventCreate(
        match_id=data.TEST_MATCH_ID_1,
        event_type=EventType.PLAYER_SPAWNED,
        player_id=data.TEST_PLAYER_ID_1,
        timestamp=data.TEST_MATCH_TIMESTAMP_EARLY,
        payload={"x": 0, "y": 1, "z": 0},
    )

    create_event(event1)
    create_event(event2)

    events = list_events()

    assert len(events) == 2

    assert events[0].timestamp == data.TEST_MATCH_TIMESTAMP_EARLY
    assert events[1].timestamp == data.TEST_MATCH_TIMESTAMP_LATE


def test_list_events_by_match_id_returns_only_events_for_that_match() -> None:
    create_test_match()
    create_test_player()
    create_match(
        MatchCreate(
            match_id=data.TEST_MATCH_ID_2,
            started_at=data.TEST_MATCH_TIMESTAMP_EARLY,
            map_name=data.TEST_MAP,
            game_mode=data.TEST_MODE,
        )
    )

    create_event(
        TelemetryEventCreate(
            match_id=data.TEST_MATCH_ID_1,
            event_type=EventType.SHOT_FIRED,
            player_id=data.TEST_PLAYER_ID_1,
            timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
            payload=data.test_payload(),
        )
    )

    create_event(
        TelemetryEventCreate(
            match_id=data.TEST_MATCH_ID_1,
            event_type=EventType.POSITION_UPDATED,
            player_id=data.TEST_PLAYER_ID_1,
            timestamp=data.TEST_MATCH_TIMESTAMP_EARLY,
            payload={"x": 0, "y": 1, "z": 0},
        )
    )

    create_event(
        TelemetryEventCreate(
            match_id=data.TEST_MATCH_ID_2,
            event_type=EventType.POSITION_UPDATED,
            player_id=data.TEST_PLAYER_ID_1,
            timestamp=data.TEST_MATCH_TIMESTAMP_EARLY,
            payload={"x": 0, "y": 1, "z": 0},
        )
    )

    events = list_events_by_match_id(data.TEST_MATCH_ID_1)

    assert len(events) == 2

    for event in events:
        assert event.match_id == data.TEST_MATCH_ID_1

    assert events[0].timestamp == data.TEST_MATCH_TIMESTAMP_EARLY
    assert events[1].timestamp == data.TEST_MATCH_TIMESTAMP_LATE


def test_list_player_match_events_returns_only_events_for_player_in_match() -> None:
    create_test_player()
    create_test_match()

    create_player(
        PlayerCreate(
            player_id=data.TEST_PLAYER_ID_2,
            display_name=data.TEST_DISPLAY_NAME_2
        )
    )
    create_match(
        MatchCreate(
            match_id=data.TEST_MATCH_ID_2,
            started_at=data.TEST_MATCH_TIMESTAMP_EARLY,
            map_name=data.TEST_MAP,
            game_mode=data.TEST_MODE
        )
    )

    event_late = create_event(
        TelemetryEventCreate(
            match_id=data.TEST_MATCH_ID_1,
            event_type=EventType.SHOT_FIRED,
            player_id=data.TEST_PLAYER_ID_1,
            timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
            payload=data.test_payload(),
        )
    )

    event_early = create_event(
        TelemetryEventCreate(
            match_id=data.TEST_MATCH_ID_1,
            event_type=EventType.SHOT_FIRED,
            player_id=data.TEST_PLAYER_ID_1,
            timestamp=data.TEST_MATCH_TIMESTAMP_EARLY,
            payload=data.test_payload(),
        )
    )

    create_event(
        TelemetryEventCreate(
            match_id=data.TEST_MATCH_ID_1,
            event_type=EventType.SHOT_FIRED,
            player_id=data.TEST_PLAYER_ID_2,
            timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
            payload=data.test_payload(),
        )
    )

    create_event(
        TelemetryEventCreate(
            match_id=data.TEST_MATCH_ID_2,
            event_type=EventType.SHOT_FIRED,
            player_id=data.TEST_PLAYER_ID_1,
            timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
            payload=data.test_payload(),
        )
    )

    events = list_player_match_events(data.TEST_MATCH_ID_1, data.TEST_PLAYER_ID_1)

    assert len(events) == 2
    assert events[0] == event_early
    assert events[1] == event_late