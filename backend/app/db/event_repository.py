# Database repository functions for telemetry events.

import uuid
from psycopg.types.json import Jsonb
from app.db.connection import get_connection
from app.schemas.events import TelemetryEventCreate, TelemetryEventRead


def create_event(event: TelemetryEventCreate) -> TelemetryEventRead:
    event_id = str(uuid.uuid4())
    match_id = event.match_id
    player_id = event.player_id
    event_type = event.event_type.value
    occurred_at = event.timestamp
    payload = Jsonb(event.payload)

    event_insert = """
        INSERT INTO telemetry_events(
            event_id,
            match_id,
            player_id,
            event_type,
            occurred_at,
            payload
            )
            VALUES(%s, %s, %s, %s, %s, %s)
    """
    event_values = (event_id, match_id, player_id, event_type, occurred_at, payload)

    with get_connection() as conn:
        conn.execute(event_insert, event_values)

    return TelemetryEventRead(event_id=event_id, **event.model_dump())


def get_event_by_id(event_id: str) -> TelemetryEventRead | None:
    query = """
        SELECT event_id, match_id, event_type, player_id, occurred_at, payload
        FROM telemetry_events
        WHERE event_id = %s
    """

    with get_connection() as conn:
        cursor = conn.execute(query, (event_id,))
        result = cursor.fetchone()

    if result is None:
        return None

    return TelemetryEventRead(
        event_id=result[0],
        match_id=result[1],
        event_type=result[2],
        player_id=result[3],
        timestamp=result[4],
        payload=result[5],
    )


def _list_query(query: str, params: tuple[object, ...] = ()) -> list[TelemetryEventRead]:
    events = []

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()

    for row in rows:
        events.append(
            TelemetryEventRead(
                event_id=row[0],
                match_id=row[1],
                event_type=row[2],
                player_id=row[3],
                timestamp=row[4],
                payload=row[5],
            )
        )

    return events

def list_events() -> list[TelemetryEventRead]:
    query = """
        SELECT event_id, match_id, event_type, player_id, occurred_at, payload
        FROM telemetry_events
        ORDER BY occurred_at
    """

    return _list_query(query)


def list_events_by_match_id(match_id: str) -> list[TelemetryEventRead]:
    query = """
        SELECT event_id, match_id, event_type, player_id, occurred_at, payload
        FROM telemetry_events
        WHERE match_id = %s
        ORDER BY occurred_at
    """

    return _list_query(query, (match_id,))


def list_player_match_events(match_id: str, player_id: str) -> list[TelemetryEventRead]:
    query = """
        SELECT event_id, match_id, event_type, player_id, occurred_at, payload
        FROM telemetry_events
        WHERE match_id = %s AND player_id = %s
        ORDER BY occurred_at
    """

    return _list_query(query, (match_id, player_id))