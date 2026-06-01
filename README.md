# MatchLens

MatchLens is a portfolio-oriented game telemetry analytics platform.

The project will ingest simulated multiplayer match events, store them, compute player and match statistics, detect anomalous player behavior, and display the results in a small dashboard.

## Project status

Early planning/setup.

## Planned MVP

- Generate simulated multiplayer match events
- Ingest events through a backend API
- Store events in PostgreSQL
- Compute player and match statistics
- Detect simple anomalies
- Display matches, player stats, and anomaly flags in a dashboard
- Provide Docker-based local setup, tests, and documentation

## Planned stack

- Backend: FastAPI with Python
- Database: PostgreSQL
- Frontend: React with TypeScript
- Analytics: pandas and scikit-learn
- Dev setup: Docker Compose
- Testing: pytest