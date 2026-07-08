from dataclasses import dataclass
from enum import StrEnum
import math

from app.schemas.events import EventType, TelemetryEventRead


DEFAULT_MAX_SPEED_UNITS_PER_SECOND = 20.0
DEFAULT_MIN_SHOTS_FOR_HIGH_ACCURACY = 10
DEFAULT_HIGH_ACCURACY_THRESHOLD = 0.8
DEFAULT_MIN_SHOT_INTERVAL_SECONDS_BY_WEAPON = {"rifle": 0.2}


class AnomalyType(StrEnum):
    IMPOSSIBLE_MOVEMENT = "impossible_movement"
    HIGH_ACCURACY = "high_accuracy"
    SUSPICIOUS_FIRE_RATE = "suspicious_fire_rate"


class AnomalySeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class AnomalyFlag:
    match_id: str
    player_id: str
    event_id: str | None
    anomaly_type: AnomalyType
    severity: AnomalySeverity
    description: str


def detect_impossible_movement(
    events: list[TelemetryEventRead],
    max_speed_units_per_second: float,
) -> list[AnomalyFlag]:
    anomalies: list[AnomalyFlag] = []

    position_events = [
        event for event in events if event.event_type == EventType.POSITION_UPDATED
    ]

    position_events.sort(key=lambda event: event.timestamp)

    previous_events_by_player: dict[str, TelemetryEventRead] = {}

    for current_event in position_events:
        error_msg = ""

        player_id = current_event.player_id

        previous_event = previous_events_by_player.get(player_id)

        if previous_event is None:
            previous_events_by_player[f"{player_id}"] = current_event
            continue

        time_delta = current_event.timestamp - previous_event.timestamp
        time_delta_seconds = time_delta.total_seconds()

        previous_x = previous_event.payload["x"]
        previous_y = previous_event.payload["y"]

        current_x = current_event.payload["x"]
        current_y = current_event.payload["y"]

        dx = previous_x - current_x
        dy = previous_y - current_y

        distance = math.hypot(dx, dy)

        if time_delta_seconds < 0:
            raise RuntimeError("Position events were not sorted by timestamp")

        if time_delta_seconds == 0:
            if distance > 0:
                error_msg = (
                    "Impossible movement: player changed position with zero time delta"
                )
        else:
            speed = distance / time_delta_seconds

            if speed > max_speed_units_per_second:
                error_msg = (
                    f"Impossible movement: speed {speed:.2f} units/s exceeds "
                    f"maximum {max_speed_units_per_second:.2f} units/s"
                )

        if error_msg:
            anomalies.append(
                AnomalyFlag(
                    match_id=current_event.match_id,
                    player_id=current_event.player_id,
                    event_id=current_event.event_id,
                    anomaly_type=AnomalyType.IMPOSSIBLE_MOVEMENT,
                    severity=AnomalySeverity.HIGH,
                    description=error_msg,
                )
            )

        previous_events_by_player[f"{player_id}"] = current_event

    return anomalies


def detect_high_accuracy(
    events: list[TelemetryEventRead],
    min_shots: int,
    accuracy_threshold: float,
) -> list[AnomalyFlag]:
    anomalies: list[AnomalyFlag] = []

    if events == []:
        return anomalies

    match_id = events[0].match_id

    shots_by_player: dict[str, int] = {}
    hits_by_player: dict[str, int] = {}

    for event in events:
        player_id = event.player_id

        if event.event_type == EventType.SHOT_FIRED:
            shots_by_player[player_id] = shots_by_player.get(player_id, 0) + 1
        elif event.event_type == EventType.PLAYER_HIT:
            hits_by_player[player_id] = hits_by_player.get(player_id, 0) + 1

    for player, shots in shots_by_player.items():
        if shots >= min_shots:
            hits = hits_by_player.get(player, 0)
            accuracy = hits / shots
            if accuracy > accuracy_threshold:
                anomalies.append(
                    AnomalyFlag(
                        match_id=match_id,
                        player_id=player,
                        event_id=None,
                        anomaly_type=AnomalyType.HIGH_ACCURACY,
                        severity=AnomalySeverity.MEDIUM,
                        description=(
                            f"Unusually high accuracy detected: {hits} hits from "
                            f"{shots} shots = {accuracy * 100:.2f}%, threshold "
                            f"{accuracy_threshold * 100:.2f}%"
                        ),
                    )
                )

    return anomalies


def detect_suspicious_fire_rate(
    events: list[TelemetryEventRead],
    min_shot_interval_seconds_by_weapon: dict[str, float],
) -> list[AnomalyFlag]:
    anomalies: list[AnomalyFlag] = []

    events = [event for event in events if event.event_type == EventType.SHOT_FIRED]

    events.sort(key=lambda event: event.timestamp)

    previous_shot_by_player_and_weapon: dict[tuple[str, str], TelemetryEventRead] = {}

    for current_event in events:
        player_id = current_event.player_id
        weapon = current_event.payload["weapon"]
        if weapon not in min_shot_interval_seconds_by_weapon:
            continue

        previous_event = previous_shot_by_player_and_weapon.get((player_id, weapon))

        if previous_event is None:
            previous_shot_by_player_and_weapon[(player_id, weapon)] = current_event
            continue

        min_shot_interval = min_shot_interval_seconds_by_weapon[weapon]

        time_delta = current_event.timestamp - previous_event.timestamp
        shot_interval = time_delta.total_seconds()

        if shot_interval < min_shot_interval:
            anomalies.append(
                AnomalyFlag(
                    match_id=current_event.match_id,
                    player_id=current_event.player_id,
                    event_id=current_event.event_id,
                    anomaly_type=AnomalyType.SUSPICIOUS_FIRE_RATE,
                    severity=AnomalySeverity.HIGH,
                    description=(
                        f"Suspicious fire rate: weapon '{weapon}' fired after "
                        f"{shot_interval:.3f}s, below minimum interval "
                        f"{min_shot_interval:.3f}s"
                    ),
                )
            )

        previous_shot_by_player_and_weapon[(player_id, weapon)] = current_event

    return anomalies


def detect_anomalies(
    events: list[TelemetryEventRead],
    max_speed_units_per_second: float = DEFAULT_MAX_SPEED_UNITS_PER_SECOND,
    min_shots_for_high_accuracy: int = DEFAULT_MIN_SHOTS_FOR_HIGH_ACCURACY,
    high_accuracy_threshold: float = DEFAULT_HIGH_ACCURACY_THRESHOLD,
    min_shot_interval_seconds_by_weapon: dict[
        str, float
    ] = DEFAULT_MIN_SHOT_INTERVAL_SECONDS_BY_WEAPON,
) -> list[AnomalyFlag]:
    anomalies: list[AnomalyFlag] = []

    anomalies += detect_impossible_movement(events, max_speed_units_per_second)
    anomalies += detect_high_accuracy(
        events, min_shots_for_high_accuracy, high_accuracy_threshold
    )
    anomalies += detect_suspicious_fire_rate(
        events, min_shot_interval_seconds_by_weapon
    )

    return anomalies
