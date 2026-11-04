import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://matchlens:matchlens_dev@127.0.0.1:5432/matchlens",
)
