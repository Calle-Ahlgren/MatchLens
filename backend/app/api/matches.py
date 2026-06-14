from fastapi import APIRouter, HTTPException

from app.db import match_repository
from app.schemas.matches import MatchCreate, MatchRead


router = APIRouter(prefix="/matches", tags=["matches"])


@router.post("")
def create_match(match: MatchCreate) -> MatchRead:
    return match_repository.create_match(match)


@router.get("")
def list_matches() -> list[MatchRead]:
    return match_repository.list_matches()


@router.get("/{match_id}")
def get_match(match_id: str) -> MatchRead:
    match = match_repository.get_match_by_id(match_id)

    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    return match
