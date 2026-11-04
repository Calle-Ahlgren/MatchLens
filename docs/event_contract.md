# Telemetry event contract

MatchLens accepts telemetry through `POST /events`. Event validation is implemented in [`backend/app/schemas/events.py`](../backend/app/schemas/events.py).

## Common fields

| Field | Meaning |
| --- | --- |
| `match_id` | Non-empty ID of an existing match |
| `event_type` | One of the six event types below |
| `player_id` | ID of the player who **owns** the event; required for all current types |
| `timestamp` | ISO 8601 event time (stored as `occurred_at` in PostgreSQL) |
| `payload` | JSON object with event-specific fields |

The API generates an `event_id` on creation. Invalid or missing required fields produce HTTP 422; references to unknown matches or players produce HTTP 404. Additional payload fields are permitted. Required numeric fields accept integers or floats, but not booleans.

## Event types

| Event type | Owner (`player_id`) | Required payload | Stat impact |
| --- | --- | --- | --- |
| `player_spawned` | Spawned player | `x`, `y`: numbers | — |
| `position_updated` | Moving player | `x`, `y`: numbers | Movement analysis |
| `shot_fired` | Shooter | `weapon`: string | Shots +1 |
| `player_hit` | Attacker | `target_player_id`: string, `damage`: number, `weapon`: string | Hits +1 |
| `player_killed` | Killer | `victim_player_id`: string, `weapon`: string | Kills +1 |
| `player_death` | Victim | `killer_player_id`: string, `weapon`: string, `x`, `y`: numbers | Deaths +1 |

**Event ownership:** The top-level `player_id` identifies whose event stream the record belongs to. Other involved players are identified inside `payload`. For example, `player_hit` belongs to the attacker, not the target. A `shot_fired` event can miss; a separate `player_hit` event records a hit.

## Example: one elimination, two player events

A single elimination can be represented by two requests to `POST /events`: one event for the killer's statistics and one for the victim's.

**Kill (owned by `player_001`):**

```json
{
  "match_id": "match_001",
  "event_type": "player_killed",
  "player_id": "player_001",
  "timestamp": "2026-11-03T12:00:02Z",
  "payload": {"victim_player_id": "player_002", "weapon": "rifle"}
}
```

**Death (owned by `player_002`):**

```json
{
  "match_id": "match_001",
  "event_type": "player_death",
  "player_id": "player_002",
  "timestamp": "2026-11-03T12:00:02Z",
  "payload": {"killer_player_id": "player_001", "weapon": "rifle", "x": 10, "y": 20}
}
```

This yields one kill for `player_001` and one death for `player_002`. Player statistics are computed by counting events in each player's match stream; accuracy is `hits / shots` (or `0` when no shots were fired).

Event-specific fields are stored in PostgreSQL `JSONB`. Required payloads are checked by Pydantic when events enter through the API; PostgreSQL itself does not enforce those JSONB field requirements.
