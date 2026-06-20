from fastapi import APIRouter, HTTPException

from app.db import match_repository
from app.db import event_repository
from app.db import player_repository
from app.schemas.matches import MatchCreate, MatchRead
from app.schemas.events import TelemetryEventRead
from app.services.player_stats_service import PlayerMatchStats, get_player_match_stats


router = APIRouter(prefix="/matches", tags=["matches"])


def _get_match_or_404(match_id: str) -> MatchRead:
    match = match_repository.get_match_by_id(match_id)

    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    return match


def _ensure_match_exists(match_id: str) -> None:
    if not match_repository.match_exists(match_id):
        raise HTTPException(status_code=404, detail="Match not found")


def _ensure_player_exists(player_id: str) -> None:
    if not player_repository.player_exists(player_id):
        raise HTTPException(status_code=404, detail="Player not found")


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
    _ensure_match_exists(match_id)

    return event_repository.list_events_by_match_id(match_id)


@router.get("/{match_id}/players/{player_id}/stats")
def get_match_player_stats(match_id: str, player_id: str) -> PlayerMatchStats:
    _ensure_match_exists(match_id)
    _ensure_player_exists(player_id)

    return get_player_match_stats(match_id, player_id)