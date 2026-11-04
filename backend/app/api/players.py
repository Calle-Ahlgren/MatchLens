from fastapi import APIRouter, HTTPException
from psycopg.errors import UniqueViolation

from app.db import player_repository
from app.schemas.players import PlayerCreate, PlayerRead

router = APIRouter(prefix="/players", tags=["players"])


@router.post("")
def create_player(player: PlayerCreate) -> PlayerRead:
    try:
        return player_repository.create_player(player)
    except UniqueViolation:
        raise HTTPException(status_code=409, detail="Player already exists")


@router.get("")
def list_players() -> list[PlayerRead]:
    return player_repository.list_players()


@router.get("/{player_id}")
def get_player(player_id: str) -> PlayerRead:
    player = player_repository.get_player_by_id(player_id)

    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return player
