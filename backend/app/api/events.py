from fastapi import APIRouter

from app.schemas.events import TelemetryEventCreate


router = APIRouter(prefix="/events", tags=["events"])

events: list[TelemetryEventCreate] = []

@router.post("")
def create_event(event: TelemetryEventCreate) -> TelemetryEventCreate:
    events.append(event)
    return event


@router.get("")
def list_events() -> list[TelemetryEventCreate]:
    return events