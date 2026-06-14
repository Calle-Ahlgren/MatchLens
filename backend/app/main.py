from fastapi import FastAPI

from app.api.events import router as events_router
from app.api.matches import router as match_router


app = FastAPI(
    title="MatchLens API",
    description="Backend API for the MatchLens game telemetry analytics platform.",
    version="0.1.0",
)


app.include_router(events_router)
app.include_router(match_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
