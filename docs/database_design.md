# MatchLens Database Schema

## Goal

TODO: Explain what the initial database schema needs to support.

## Tables

### matches

TODO: Describe what one row in this table represents.

Columns:

| Column | Type | Purpose |
|---|---|---|
| match_id | text | TODO |
| map_name | text | TODO |
| game_mode | text | TODO |
| started_at | timestamptz | TODO |
| ended_at | timestamptz | TODO |
| created_at | timestamptz | TODO |

### players

TODO: Describe what one row in this table represents.

Columns:

| Column | Type | Purpose |
|---|---|---|
| player_id | text | TODO |
| display_name | text | TODO |
| created_at | timestamptz | TODO |

### telemetry_events

TODO: Describe what one row in this table represents.

Columns:

| Column | Type | Purpose |
|---|---|---|
| event_id | uuid | TODO |
| match_id | text | TODO |
| player_id | text | TODO |
| event_type | text | TODO |
| timestamp | timestamptz | TODO |
| payload | jsonb | TODO |
| created_at | timestamptz | TODO |

## Relationships

TODO: Explain how telemetry_events connects to matches and players.

## Design choices

### Why store event payload as JSONB?

TODO: Explain why event-specific data belongs in payload.

### Why keep match_id and player_id as text?

TODO: Explain why readable simulator IDs are useful for the MVP.

### Why not add stats/anomaly tables yet?

TODO: Explain why raw event storage comes first.