from fastapi import FastAPI

app = FastAPI(
    title="MatchLens API",
    description="Backend API for the MatchLens game telemetry analytics platform.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}