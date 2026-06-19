import pytest

from app.db.event_repository import create_event
from app.db.player_repository import create_player
from app.schemas.events import EventType, TelemetryEventRead, TelemetryEventCreate
from app.schemas.players import PlayerCreate
from app.services.player_stats_service import (
    get_player_match_stats,
    compute_player_match_stats,
)
from tests.db_test_utils import create_test_event, clear_database_tables
from tests import sample_data as data


@pytest.fixture
def clear_test_database() -> None:
    clear_database_tables()

    yield

    clear_database_tables()


def test_compute_player_match_stats_counts_basic_combat_events() -> None:
    event1 = TelemetryEventRead(
        match_id=data.TEST_MATCH_ID_1,
        event_type=EventType.SHOT_FIRED,
        player_id=data.TEST_PLAYER_ID_1,
        timestamp=data.TEST_MATCH_TIMESTAMP_EARLY,
        payload=data.test_payload(),
        event_id="event_001",
    )

    event2 = TelemetryEventRead(
        match_id=data.TEST_MATCH_ID_1,
        event_type=EventType.SHOT_FIRED,
        player_id=data.TEST_PLAYER_ID_1,
        timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
        payload=data.test_payload(),
        event_id="event_002",
    )

    event3 = TelemetryEventRead(
        match_id=data.TEST_MATCH_ID_1,
        event_type=EventType.PLAYER_HIT,
        player_id=data.TEST_PLAYER_ID_1,
        timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
        payload={"target_player_id": data.TEST_PLAYER_ID_2},
        event_id="event_003",
    )

    event4 = TelemetryEventRead(
        match_id=data.TEST_MATCH_ID_1,
        event_type=EventType.PLAYER_KILLED,
        player_id=data.TEST_PLAYER_ID_1,
        timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
        payload={"victim_player_id": data.TEST_PLAYER_ID_2},
        event_id="event_004",
    )

    event5 = TelemetryEventRead(
        match_id=data.TEST_MATCH_ID_1,
        event_type=EventType.PLAYER_DEATH,
        player_id=data.TEST_PLAYER_ID_1,
        timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
        payload={"x": 0, "y": 0, "z": 1, "killer_player_id": "player_003"},
        event_id="event_005",
    )

    events = [event1, event2, event3, event4, event5]

    stats = compute_player_match_stats(
        events, data.TEST_MATCH_ID_1, data.TEST_PLAYER_ID_1
    )

    assert stats.shots_fired == 2
    assert stats.hits == 1
    assert stats.kills == 1
    assert stats.deaths == 1
    assert stats.accuracy == 0.5


def test_get_player_match_stats_loads_events_and_computes_stats(
    clear_test_database,
) -> None:
    create_test_event()
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
            event_type=EventType.PLAYER_HIT,
            player_id=data.TEST_PLAYER_ID_1,
            timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
            payload={"target_player_id": data.TEST_PLAYER_ID_2},
        )
    )

    create_event(
        TelemetryEventCreate(
            match_id=data.TEST_MATCH_ID_1,
            event_type=EventType.PLAYER_KILLED,
            player_id=data.TEST_PLAYER_ID_1,
            timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
            payload={"victim_player_id": data.TEST_PLAYER_ID_2},
        )
    )

    create_event(
        TelemetryEventCreate(
            match_id=data.TEST_MATCH_ID_1,
            event_type=EventType.PLAYER_DEATH,
            player_id=data.TEST_PLAYER_ID_1,
            timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
            payload={"x": 0, "y": 0, "z": 1, "killer_player_id": "player_003"},
        )
    )

    create_player(
        PlayerCreate(
            player_id=data.TEST_PLAYER_ID_2, display_name=data.TEST_DISPLAY_NAME_2
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

    player_stats = get_player_match_stats(data.TEST_MATCH_ID_1, data.TEST_PLAYER_ID_1)

    assert player_stats.shots_fired == 2
    assert player_stats.hits == 1
    assert player_stats.kills == 1
    assert player_stats.deaths == 1
    assert player_stats.accuracy == 0.5
