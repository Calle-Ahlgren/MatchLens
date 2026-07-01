from dataclasses import dataclass
from enum import StrEnum
import math

from app.schemas.events import EventType, TelemetryEventRead


DEFAULT_MAX_SPEED_UNITS_PER_SECOND = 20.0


class AnomalyType(StrEnum):
    IMPOSSIBLE_MOVEMENT = "impossible_movement"


class AnomalySeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class AnomalyFlag:
    match_id: str
    player_id: str
    event_id: str
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
                    player_id=current_event.player_id or "",
                    event_id=current_event.event_id,
                    anomaly_type=AnomalyType.IMPOSSIBLE_MOVEMENT,
                    severity=AnomalySeverity.HIGH,
                    description=error_msg,
                )
            )

        previous_events_by_player[f"{player_id}"] = current_event

    return anomalies


def detect_anomalies(
    events: list[TelemetryEventRead],
    max_speed_units_per_second: float = DEFAULT_MAX_SPEED_UNITS_PER_SECOND,
) -> list[AnomalyFlag]:
    anomalies: list[AnomalyFlag] = []

    anomalies += detect_impossible_movement(events, max_speed_units_per_second)

    return anomalies
