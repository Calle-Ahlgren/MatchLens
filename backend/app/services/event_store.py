from app.schemas.events import TelemetryEventCreate

_events: list[TelemetryEventCreate] = []


def add_event(event: TelemetryEventCreate) -> TelemetryEventCreate:
    _events.append(event)
    return event


def get_events() -> list[TelemetryEventCreate]:
    return _events