from fastapi import APIRouter, HTTPException
from psycopg.errors import ForeignKeyViolation

from app.db import event_repository
from app.schemas.events import TelemetryEventCreate, TelemetryEventRead

router = APIRouter(prefix="/events", tags=["events"])


@router.post("")
def create_event(event: TelemetryEventCreate) -> TelemetryEventRead:
    try:
        return event_repository.create_event(event)
    except ForeignKeyViolation as e:
        if e.diag.constraint_name == "telemetry_events_match_id_fkey":
            raise HTTPException(status_code=404, detail="Match not found")
        elif e.diag.constraint_name == "telemetry_events_player_id_fkey":
            raise HTTPException(status_code=404, detail="Player not found")
        raise


@router.get("")
def list_events() -> list[TelemetryEventRead]:
    return event_repository.list_events()


@router.get("/{event_id}")
def get_event(event_id: str) -> TelemetryEventRead:
    event = event_repository.get_event_by_id(event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event
