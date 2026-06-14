from fastapi import APIRouter, HTTPException

from app.db import match_repository
from app.schemas.matches import MatchCreate, MatchRead


router = APIRouter(prefix="/matches", tags=["matches"])

@router.post("")
def create_match(match: MatchCreate) -> MatchRead:
    match_repository.create_match(
        match.match_id, 
        match.started_at, 
        match.map_name, 
        match.game_mode
    )
    return MatchRead(**match.model_dump())

@router.get("/{match_id}")
def get_match(match_id: str) -> MatchRead:
    match = match_repository.get_match_by_id(match_id)

    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    return match


