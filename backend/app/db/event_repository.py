# Database repository functions for telemetry events.
# These are not wired into the API yet.

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