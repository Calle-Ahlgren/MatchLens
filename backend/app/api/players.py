from fastapi import APIRouter, HTTPException

from app.db import player_repository
from app.schemas.players import PlayerCreate, PlayerRead


router = APIRouter(prefix="/players", tags=["players"])


@router.post("")
def create_player(player: PlayerCreate) -> PlayerRead:
    return player_repository.create_player(player)


@router.get("")
def list_players() -> list[PlayerRead]:
    return player_repository.list_players()


@router.get("/{player_id}")
def get_player(player_id: str) -> PlayerRead:
    player = player_repository.get_player_by_id(player_id)

    if player is None:
        raise HTTPException(status_code=404, detail="player not found")

    return player