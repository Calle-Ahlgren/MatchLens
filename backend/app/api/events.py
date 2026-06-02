from fastapi import APIRouter

from app.schemas.events import TelemetryEventCreate


router = APIRouter(prefix="/events", tags=["events"])


@router.post("")
def create_event(event: TelemetryEventCreate) -> TelemetryEventCreate:
    return event