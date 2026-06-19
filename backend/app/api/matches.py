from fastapi import APIRouter, HTTPException

from app.db import match_repository
from app.db import event_repository
from app.schemas.matches import MatchCreate, MatchRead
from app.schemas.events import TelemetryEventRead


router = APIRouter(prefix="/matches", tags=["matches"])


def _get_match_or_404(match_id: str) -> MatchRead:
    match = match_repository.get_match_by_id(match_id)

    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    return match


@router.post("")
def create_match(match: MatchCreate) -> MatchRead:
    return match_repository.create_match(match)


@router.get("")
def list_matches() -> list[MatchRead]:
    return match_repository.list_matches()


@router.get("/{match_id}")
def get_match(match_id: str) -> MatchRead:
    return _get_match_or_404(match_id)


@router.get("/{match_id}/events")
def list_match_events(match_id: str) -> list[TelemetryEventRead]:
    _get_match_or_404(match_id)

    return event_repository.list_events_by_match_id(match_id)
