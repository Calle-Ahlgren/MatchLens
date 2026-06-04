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

## Local development setup

### Prerequisites

- Python 3.12+
- Docker Desktop

### Start PostgreSQL

MatchLens uses Docker Compose to run a local PostgreSQL database for development.

From the project root:

```powershell
docker compose up -d
```

This starts PostgreSQL in the background using the configuration in `docker-compose.yml`.

### Check that PostgreSQL is running

```powershell
docker compose ps
```

You should see a `postgres` service with status `Up` and port `5432` exposed.

### Verify that the schema loaded

List database tables:

```powershell
docker compose exec postgres psql -U matchlens -d matchlens -c "\dt"
```

Expected tables:

```text
matches
players
telemetry_events
```

List indexes:

```powershell
docker compose exec postgres psql -U matchlens -d matchlens -c "\di"
```

You should see indexes for the primary keys and the custom telemetry event indexes.

### Stop PostgreSQL

```powershell
docker compose down
```

This stops the container. The database data is kept in the Docker volume `matchlens_postgres_data`.
