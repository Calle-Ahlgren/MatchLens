from fastapi import APIRouter, HTTPException

from app.schemas.events import TelemetryEventCreate, TelemetryEventRead
from app.services.event_store import add_event, get_event_by_id, get_events


router = APIRouter(prefix="/events", tags=["events"])


@router.post("")
def create_event(event: TelemetryEventCreate) -> TelemetryEventRead:
    return add_event(event)


@router.get("")
def list_events() -> list[TelemetryEventRead]:
    return get_events()


@router.get("/{event_id}")
def get_event(event_id: str) -> TelemetryEventRead:
    event = get_event_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event
