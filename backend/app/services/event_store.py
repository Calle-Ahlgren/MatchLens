import uuid

from app.schemas.events import TelemetryEventCreate, TelemetryEventRead


_events: list[TelemetryEventRead] = []


def add_event(event: TelemetryEventCreate) -> TelemetryEventRead:
    stored_event = TelemetryEventRead(event_id=str(uuid.uuid4()), **event.model_dump())
    _events.append(stored_event)
    return stored_event


def get_events() -> list[TelemetryEventRead]:
    return _events


def clear_events() -> None:
    _events.clear()


def get_event_by_id(event_id: str) -> TelemetryEventRead | None:
    for event in _events:
        if event.event_id == event_id:
            return event
    return None
