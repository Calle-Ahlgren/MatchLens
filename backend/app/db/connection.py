import psycopg
from psycopg import Connection

from app.core.config import DATABASE_URL


def get_connection() -> Connection:

    return psycopg.connect(DATABASE_URL)
