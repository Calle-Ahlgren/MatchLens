"""Database connection helpers for MatchLens.

This module is intentionally small for now.
It only knows how to open a PostgreSQL connection using DATABASE_URL.

Later, services/repositories will use this instead of the in-memory event store.
"""

import psycopg
from psycopg import Connection

from app.core.config import DATABASE_URL


def get_connection() -> Connection:
    """Open a new PostgreSQL connection.

    TODO:
    Later we may add connection pooling or FastAPI dependency injection.

    For now, this function gives us one simple place to create database
    connections.
    """
    return psycopg.connect(DATABASE_URL)
    