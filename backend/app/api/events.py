from fastapi import APIRouter

from app.schemas.events import TelemetryEventCreate, TelemetryEventRead
from app.services.event_store import add_event, get_events


router = APIRouter(prefix="/events", tags=["events"])


@router.post("")
def create_event(event: TelemetryEventCreate) -> TelemetryEventRead:
    return add_event(event)


@router.get("")
def list_events() -> list[TelemetryEventRead]:
    return get_events()