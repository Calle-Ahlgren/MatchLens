import os

import pytest

os.environ["DATABASE_URL"] = (
    "postgresql://matchlens:matchlens_dev@127.0.0.1:5432/matchlens_test"
)


@pytest.fixture
def clear_test_database() -> None:
    from tests.db_test_utils import clear_database_tables

    clear_database_tables()

    yield

    clear_database_tables()
