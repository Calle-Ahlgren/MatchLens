from fastapi import APIRouter
from app.services.event_store import add_event, get_events
from app.schemas.events import TelemetryEventCreate


router = APIRouter(prefix="/events", tags=["events"])


@router.post("")
def create_event(event: TelemetryEventCreate) -> TelemetryEventCreate:
    return add_event(event)


@router.get("")
def list_events() -> list[TelemetryEventCreate]:
    return get_events()