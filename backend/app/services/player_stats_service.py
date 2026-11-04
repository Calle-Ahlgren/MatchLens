from dataclasses import dataclass

from app.db.event_repository import list_player_match_events
from app.schemas.events import EventType, TelemetryEventRead


@dataclass
class PlayerMatchStats:
    match_id: str
    player_id: str
    shots_fired: int
    hits: int
    kills: int
    deaths: int
    accuracy: float


def compute_player_match_stats(
    events: list[TelemetryEventRead],
    match_id: str,
    player_id: str,
) -> PlayerMatchStats:
    shots_fired, hits, kills, deaths = 0, 0, 0, 0

    for event in events:
        match event.event_type:
            case EventType.SHOT_FIRED:
                shots_fired += 1
            case EventType.PLAYER_HIT:
                hits += 1
            case EventType.PLAYER_KILLED:
                kills += 1
            case EventType.PLAYER_DEATH:
                deaths += 1

    accuracy = 0.0

    if shots_fired != 0:
        accuracy = hits / shots_fired

    return PlayerMatchStats(
        match_id=match_id,
        player_id=player_id,
        shots_fired=shots_fired,
        hits=hits,
        kills=kills,
        deaths=deaths,
        accuracy=accuracy,
    )


def get_player_match_stats(match_id: str, player_id: str) -> PlayerMatchStats:
    events = list_player_match_events(match_id, player_id)
    return compute_player_match_stats(events, match_id, player_id)
