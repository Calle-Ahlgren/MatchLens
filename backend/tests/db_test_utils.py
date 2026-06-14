from app.db.connection import get_connection
from app.db.match_repository import create_match
from app.db.player_repository import create_player
from app.db.event_repository import create_event
from app.schemas.matches import MatchCreate, MatchRead
from app.schemas.players import PlayerCreate, PlayerRead
from app.schemas.events import EventType, TelemetryEventCreate, TelemetryEventRead
from tests import sample_data as data


def clear_database_tables() -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM telemetry_events")
        conn.execute("DELETE FROM players")
        conn.execute("DELETE FROM matches")


def create_test_match() -> MatchRead:
    match = MatchCreate(
        match_id=data.TEST_MATCH_ID_1,
        started_at=data.TEST_MATCH_TIMESTAMP_EARLY,
        map_name=data.TEST_MAP,
        game_mode=data.TEST_MODE,
    )

    return create_match(match)


def create_test_player() -> PlayerRead:
    player = PlayerCreate(
        player_id=data.TEST_PLAYER_ID_1,
        display_name=data.TEST_DISPLAY_NAME,
    )
    return create_player(player)


def create_test_event() -> TelemetryEventRead:
    create_test_match()
    create_test_player()

    event = TelemetryEventCreate(
        match_id=data.TEST_MATCH_ID_1,
        event_type=EventType.SHOT_FIRED,
        player_id=data.TEST_PLAYER_ID_1,
        timestamp=data.TEST_MATCH_TIMESTAMP_EARLY,
        payload=data.test_payload(),
    )

    return create_event(event)