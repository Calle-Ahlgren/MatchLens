-- MatchLens initial PostgreSQL schema.
-- Defines the first persistent storage model for matches, players,
-- and raw telemetry events.
--
-- This file is intentionally small for the MVP.
-- It does not include analytics tables or backend database wiring yet.

DROP TABLE IF EXISTS telemetry_events;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches;

CREATE TABLE matches (
    match_id TEXT PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ,
    map_name TEXT NOT NULL,
    game_mode TEXT NOT NULL,
    CHECK (ended_at IS NULL OR ended_at > started_at)
);

CREATE TABLE players (
    player_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE TABLE telemetry_events (
    event_id TEXT PRIMARY KEY,
    match_id TEXT NOT NULL REFERENCES matches(match_id),
    player_id TEXT NOT NULL REFERENCES players(player_id),
    event_type TEXT NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL,
    payload JSONB NOT NULL,
    inserted_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_telemetry_events_match_occurred_at
ON telemetry_events(match_id, occurred_at);

CREATE INDEX idx_telemetry_events_player_id
ON telemetry_events(player_id);

CREATE INDEX idx_telemetry_events_event_type
ON telemetry_events(event_type);