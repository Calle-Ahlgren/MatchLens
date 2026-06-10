Phase 0: Backend foundation
Status: mostly done

- FastAPI app
- health endpoint
- event schemas
- in-memory event API
- pytest tests
- Ruff formatting

Phase 1: Database design and local PostgreSQL
Status: current phase

- design initial tables
- write database/init.sql
- set up PostgreSQL with Docker Compose
- verify schema loads correctly

Phase 2: Backend database integration

- add database connection settings
- create DB access layer
- replace in-memory event store with PostgreSQL
- update tests
- keep API behavior mostly the same

Phase 3: Telemetry simulator

- generate fake matches
- generate players
- generate events
- send events to backend API
- produce believable match timelines

Phase 4: Statistics pipeline

- compute match summaries
- compute player stats
- kills/deaths/shots/hits/accuracy/movement
- store or expose stats through API

Phase 5: Anomaly detection

- define simple rules first
- impossible movement
- suspicious accuracy
- abnormal kill rate
- expose anomaly flags through API

Phase 6: Dashboard

- React + TypeScript frontend
- matches page
- match detail page
- player stats
- anomaly flags

Phase 7: Portfolio polish

- README
- screenshots
- architecture notes
- setup instructions
- test instructions
- final cleanup