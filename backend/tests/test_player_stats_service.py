from app.schemas.events import EventType, TelemetryEventRead
from app.services.player_stats_service import (
    compute_player_match_stats,
)
from tests import sample_data as data


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
        payload={
            "target_player_id": data.TEST_PLAYER_ID_2,
            "damage": 34,
            "weapon": "rifle",
        },
        event_id="event_003",
    )

    event4 = TelemetryEventRead(
        match_id=data.TEST_MATCH_ID_1,
        event_type=EventType.PLAYER_KILLED,
        player_id=data.TEST_PLAYER_ID_1,
        timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
        payload={
            "victim_player_id": data.TEST_PLAYER_ID_2,
            "weapon": "rifle",
        },
        event_id="event_004",
    )

    event5 = TelemetryEventRead(
        match_id=data.TEST_MATCH_ID_1,
        event_type=EventType.PLAYER_DEATH,
        player_id=data.TEST_PLAYER_ID_1,
        timestamp=data.TEST_MATCH_TIMESTAMP_LATE,
        payload={
            "killer_player_id": "player_003",
            "weapon": "rifle",
            "x": 0,
            "y": 0,
        },
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
