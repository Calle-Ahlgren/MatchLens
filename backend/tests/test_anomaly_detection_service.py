from datetime import UTC, datetime, timedelta

from app.schemas.events import EventType, TelemetryEventRead
from app.services.anomaly_detection_service import (
    AnomalySeverity,
    AnomalyType,
    detect_impossible_movement,
)


TIMESTAMP = datetime(2026, 6, 2, 18, 30, 0, tzinfo=UTC)


def make_position_event(
    event_id: str,
    timestamp: datetime,
    x: float,
    y: float,
    player_id: str = "player_001",
) -> TelemetryEventRead:
    return TelemetryEventRead(
        match_id="match_001",
        event_type=EventType.POSITION_UPDATED,
        player_id=player_id,
        timestamp=timestamp,
        payload={
            "x": x,
            "y": y,
        },
        event_id=event_id,
    )


def test_detect_impossible_movement_flags_diagonal_position_jump() -> None:

    events = [
        make_position_event("event_001", TIMESTAMP, 0, 0),
        make_position_event("event_002", TIMESTAMP + timedelta(seconds=1), 30, 40),
    ]

    anomalies = detect_impossible_movement(
        events,
        max_speed_units_per_second=20,
    )

    assert len(anomalies) == 1

    anomaly = anomalies[0]

    assert anomaly.event_id == "event_002"
    assert anomaly.match_id == "match_001"
    assert anomaly.player_id == "player_001"
    assert anomaly.anomaly_type == AnomalyType.IMPOSSIBLE_MOVEMENT
    assert anomaly.severity == AnomalySeverity.HIGH
    assert "speed" in anomaly.description.lower()


def test_detect_impossible_movement_flags_position_change_with_same_timestamp() -> None:
    events = [
        make_position_event("event_001", TIMESTAMP, 0, 0),
        make_position_event("event_002", TIMESTAMP, 30, 40),
    ]

    anomalies = detect_impossible_movement(
        events,
        max_speed_units_per_second=20,
    )

    assert len(anomalies) == 1

    anomaly = anomalies[0]

    assert anomaly.event_id == "event_002"
    assert anomaly.anomaly_type == AnomalyType.IMPOSSIBLE_MOVEMENT
    assert anomaly.severity == AnomalySeverity.HIGH
    assert "zero time" in anomaly.description.lower()


def test_detect_impossible_movement_does_not_flag_normal_movement() -> None:
    events = [
        make_position_event("event_001", TIMESTAMP, 0, 0),
        make_position_event("event_002", TIMESTAMP + timedelta(seconds=1), 3, 4),
    ]

    anomalies = detect_impossible_movement(
        events,
        max_speed_units_per_second=20,
    )

    assert anomalies == []


def test_detect_impossible_movement_does_not_compare_different_players() -> None:
    events = [
        make_position_event("event_001", TIMESTAMP, 0, 0),
        make_position_event(
            "event_002",
            TIMESTAMP + timedelta(seconds=1),
            100,
            0,
            player_id="player_002",
        ),
    ]

    anomalies = detect_impossible_movement(
        events,
        max_speed_units_per_second=20,
    )

    assert anomalies == []


def test_detect_impossible_movement_returns_multiple_anomalies() -> None:
    events = [
        make_position_event("event_001", TIMESTAMP, 0, 0),
        make_position_event(
            "event_002",
            TIMESTAMP + timedelta(seconds=1),
            30,
            40,
            player_id="player_001",
        ),
        make_position_event(
            "event_003",
            TIMESTAMP + timedelta(seconds=2),
            60,
            80,
            player_id="player_001",
        ),
    ]

    anomalies = detect_impossible_movement(
        events,
        max_speed_units_per_second=20,
    )

    assert len(anomalies) == 2

    assert anomalies[0].event_id == "event_002"
    assert anomalies[1].event_id == "event_003"
    assert anomalies[0].anomaly_type == AnomalyType.IMPOSSIBLE_MOVEMENT
    assert anomalies[1].anomaly_type == AnomalyType.IMPOSSIBLE_MOVEMENT


def test_detect_impossible_movement_handles_unsorted_events() -> None:
    events = [
        make_position_event(
            "event_002",
            TIMESTAMP + timedelta(seconds=1),
            30,
            40,
            player_id="player_001",
        ),
        make_position_event("event_001", TIMESTAMP, 0, 0),
    ]

    anomalies = detect_impossible_movement(
        events,
        max_speed_units_per_second=20,
    )

    assert len(anomalies) == 1
    assert anomalies[0].event_id == "event_002"
