import pytest
import sample_data as data

from app.db.event_repository import (
    create_event,
    get_event_by_id,
    list_events,
    list_events_by_match_id,
    list_player_match_events,
)
from app.db.match_repository import create_match
from app.db.player_repository import create_player
from app.schemas.events import EventType, TelemetryEventCreate
from app.schemas.matches import MatchCreate
from app.schemas.players import PlayerCreate
from tests.db_test_utils import (
    create_test_event,
    create_test_match,
    create_test_player,
)

pytestmark = pytest.mark.usefixtures("clear_test_database")


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
            player_id=data.TEST_PLAYER_ID_2, display_name=data.TEST_DISPLAY_NAME_2
        )
    )
    create_match(
        MatchCreate(
            match_id=data.TEST_MATCH_ID_2,
            started_at=data.TEST_MATCH_TIMESTAMP_EARLY,
            map_name=data.TEST_MAP,
            game_mode=data.TEST_MODE,
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
