# MatchLens MVP Spec

## Goal

Build a small, portfolio-ready game telemetry analytics platform.

A reviewer should be able to clone the repository, run the project locally, generate simulated match data, and inspect match/player statistics and anomaly flags.

## MVP Features

1. Simulate multiplayer match events.
2. Ingest events through a backend API.
3. Store events in PostgreSQL.
4. Compute basic player and match statistics.
5. Detect simple anomalous behavior.
6. Display results in a small dashboard.
7. Include tests, Docker setup, and documentation.

## Non-goals for MVP

- No real game client.
- No authentication.
- No cloud deployment.
- No Kafka or complex streaming.
- No deep learning.
- No production anti-cheat claims.

## Success Criteria

The MVP is successful when:

- The system can generate fake match data.
- The backend can ingest and store events.
- The database stores matches, players, events, stats, and anomaly flags.
- The dashboard shows useful information.
- The project can be run locally by following the README.