"""Application configuration for MatchLens.

This module centralizes environment-based settings so the rest of the
backend does not hardcode infrastructure details like database URLs.
"""

import os


# TODO:
# Later, this value will be used by the database connection layer.
#
# For now, it only gives us a single agreed-upon place where the backend
# can read the PostgreSQL connection string.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://matchlens:matchlens_dev@localhost:5432/matchlens",
)
