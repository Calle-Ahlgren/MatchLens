# MatchLens

MatchLens is a portfolio-oriented game telemetry analytics platform.

The project simulates multiplayer match telemetry, ingests it through a FastAPI backend, stores it in PostgreSQL, computes player match statistics, and prepares the foundation for anomaly detection and a future dashboard.

The goal is to demonstrate backend development, database design, data processing, testing, documentation, and a clear connection to games.

## Project status

Current MVP progress:

* FastAPI backend is implemented.
* PostgreSQL runs locally through Docker Compose.
* Initial database schema exists for matches, players, and telemetry events.
* Backend API can create and retrieve matches, players, and telemetry events.
* Match-scoped event listing is implemented.
* Player match statistics are computed from stored telemetry events.
* A simulator can generate sample match data.
* A simulator upload script can post generated matches, players, and events to the backend.
* Backend tests are implemented with pytest.
* Event semantics are documented in `docs/event_contract.md`.

Not implemented yet:

* Anomaly detection.
* Frontend dashboard.
* Persistent analytics/statistics tables.
* Event-type-specific payload validation.
* Authentication.
* Cloud deployment.

These are intentionally left out for now to keep the MVP small and finishable.

## Current features

### Backend API

Implemented endpoints include:

```text
GET  /health

POST /matches
GET  /matches
GET  /matches/{match_id}
GET  /matches/{match_id}/events
GET  /matches/{match_id}/players/{player_id}/stats

POST /players
GET  /players
GET  /players/{player_id}

POST /events
GET  /events
GET  /events/{event_id}
```

### Database

The current PostgreSQL schema contains:

```text
matches
players
telemetry_events
```

Telemetry events reference matches and players. Event payloads are stored as flexible JSONB.

### Simulator

The simulator can:

* create a sample match
* create sample players
* create ordered telemetry events
* write generated data to `simulator/output/sample_match.json`
* upload generated match data to the backend API

Generated simulator output is ignored by Git and should not be committed.

### Player match statistics

The backend currently computes simple player statistics from event streams:

```text
shots_fired
hits
kills
deaths
accuracy
```

Stats are computed for a specific player in a specific match.

The current event model is player-stream based:

```text
event.player_id = the player whose event stream the event belongs to
```

For example:

* `shot_fired` belongs to the shooter
* `player_hit` belongs to the attacker
* `player_killed` belongs to the killer
* `player_death` belongs to the player who died

See `docs/event_contract.md` for the current event contract.

## Tech stack

Current stack:

* Backend: FastAPI, Python
* Database: PostgreSQL
* Database driver: psycopg
* Local infrastructure: Docker Compose
* Testing: pytest, FastAPI TestClient
* Formatting/linting: Ruff
* Simulator: Python standard library

Planned later:

* Frontend: React with TypeScript
* Analytics/anomaly detection: pandas and scikit-learn

## Project structure

```text
matchlens/
  backend/
    app/
      api/
        events.py
        matches.py
        players.py
      core/
        config.py
      db/
        connection.py
        event_repository.py
        match_repository.py
        player_repository.py
      schemas/
        events.py
        matches.py
        players.py
      services/
        player_stats_service.py
      main.py
    tests/
    requirements.txt

  database/
    init.sql

  docs/
    event_contract.md

  simulator/
    api_client.py
    generate_matches.py
    upload_sample_match.py

  docker-compose.yml
  README.md
```

## Local development setup

These commands assume PowerShell on Windows.

### Prerequisites

Install:

* Python 3.12+
* Docker Desktop
* Git

### 1. Start PostgreSQL

From the project root:

```powershell
docker compose up -d
```

Check that PostgreSQL is running:

```powershell
docker compose ps
```

You should see the `postgres` service running and exposing port `5432`.

### 2. Verify the database schema

From the project root:

```powershell
docker compose exec postgres psql -U matchlens -d matchlens -c "\dt"
```

Expected tables:

```text
matches
players
telemetry_events
```

To list indexes:

```powershell
docker compose exec postgres psql -U matchlens -d matchlens -c "\di"
```

### 3. Set up the backend environment

From the project root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the backend API

From the `backend` folder, with the virtual environment active:

```powershell
python -m uvicorn app.main:app --reload
```

The API should now be available at:

```text
http://127.0.0.1:8000
```

FastAPI docs are available at:

```text
http://127.0.0.1:8000/docs
```

Test the health endpoint:

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/health
```

Expected response:

```text
status
------
ok
```

## Running the simulator

Use a second PowerShell terminal from the project root.

### Generate local sample data

```powershell
python .\simulator\generate_matches.py
```

This writes generated sample data to:

```text
simulator/output/sample_match.json
```

The output folder is generated locally and should not be committed.

### Upload sample match data to the API

Make sure the backend is running first.

From the project root:

```powershell
python .\simulator\upload_sample_match.py
```

Expected output shape:

```text
Uploaded match: match_<unique_id>
Uploaded players: 4
Uploaded events: 16
```

The upload script creates one match, four players, and sixteen telemetry events.

## Manual API checks

### List matches

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/matches | ConvertTo-Json -Depth 5
```

### List players

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/players | ConvertTo-Json -Depth 5
```

### List all events

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/events | ConvertTo-Json -Depth 8
```

### List events for one match

Replace `<match_id>` with an actual match ID.

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/matches/<match_id>/events | ConvertTo-Json -Depth 8
```

### Get player stats for one match

Replace `<match_id>` and `<player_id>` with actual IDs.

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/matches/<match_id>/players/<player_id>/stats | ConvertTo-Json -Depth 5
```

Expected response shape:

```json
{
  "match_id": "match_example",
  "player_id": "player_example",
  "shots_fired": 1,
  "hits": 1,
  "kills": 1,
  "deaths": 0,
  "accuracy": 1.0
}
```

Actual values depend on which player is queried and which events belong to that player's event stream.

## Running tests

From the `backend` folder, with the virtual environment active:

```powershell
python -m pytest
```

Run Ruff checks:

```powershell
python -m ruff check .
python -m ruff format --check .
```

## Database persistence

The PostgreSQL container uses a Docker volume.

Stopping the database keeps stored data:

```powershell
docker compose down
```

Stopping the database and deleting stored data:

```powershell
docker compose down -v
```

Use `docker compose down -v` when you want a clean local database.

## Current design notes

### Event ownership

Telemetry events are currently player-stream based.

The top-level `player_id` identifies the player whose event stream the event belongs to. Other involved players are stored in the event payload.

Example:

```json
{
  "event_type": "player_killed",
  "player_id": "player_001",
  "payload": {
    "victim_player_id": "player_002",
    "weapon": "rifle"
  }
}
```

This means `player_001` receives one kill in player statistics.

A corresponding death event may also exist:

```json
{
  "event_type": "player_death",
  "player_id": "player_002",
  "payload": {
    "killer_player_id": "player_001",
    "weapon": "rifle"
  }
}
```

This means `player_002` receives one death in player statistics.

This duplication is intentional for the current MVP because stats are computed from each player's own event stream.

### Payload validation

The backend currently validates top-level event fields:

```text
match_id
event_type
player_id
timestamp
payload
```

It also restricts event types to known values.

The backend does not yet validate event-type-specific payload fields. For example, it does not yet enforce that `player_hit` must include `target_player_id`, `damage`, and `weapon`.

Payload validation is planned as a later backend improvement.

## Planned next milestones

### 1. Event payload validation

Add validation for required payload fields per event type.

Examples:

```text
shot_fired:
  weapon

player_hit:
  target_player_id
  damage
  weapon

player_killed:
  victim_player_id
  weapon

player_death:
  killer_player_id
  weapon
```

### 2. Anomaly detection foundation

Add simple anomaly detection rules, such as:

```text
impossible movement speed
unusually high accuracy
abnormal kill rate
```

### 3. Analytics output

Expose anomaly flags and summary data through the backend API.

### 4. Frontend dashboard

Build a small React dashboard showing:

```text
matches
players
player stats
telemetry summaries
anomaly flags
```

## Non-goals for the current MVP

The following are intentionally out of scope for now:

* Kafka or message queues
* Authentication
* Cloud deployment
* Deep learning
* Complex live ingestion
* Large-scale distributed processing
* Production-grade observability

The priority is a small, polished, end-to-end project that is easy for a reviewer to run and understand.