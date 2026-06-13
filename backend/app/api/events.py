from fastapi import APIRouter, HTTPException

from app.db import event_repository
from app.schemas.events import TelemetryEventCreate, TelemetryEventRead

router = APIRouter(prefix="/events", tags=["events"])

@router.post("")
def create_event(event: TelemetryEventCreate) -> TelemetryEventRead:
    return event_repository.create_event(event)


@router.get("")
def list_events() -> list[TelemetryEventRead]:
    return event_repository.list_events()


@router.get("/{event_id}")
def get_event(event_id: str) -> TelemetryEventRead:
    event = event_repository.get_event_by_id(event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event
