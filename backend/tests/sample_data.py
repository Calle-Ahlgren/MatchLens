from datetime import UTC, datetime

TEST_MATCH_ID_1 = "match_001"
TEST_MATCH_ID_2 = "match_002"
TEST_MATCH_TIMESTAMP_EARLY = datetime(2026, 1, 1, 1, 1, 1, tzinfo=UTC)
TEST_MATCH_TIMESTAMP_LATE = datetime(2026, 1, 1, 2, 1, 1, tzinfo=UTC)
TEST_PLAYER_ID_1 = "player_001"
TEST_PLAYER_ID_2 = "player_002"
TEST_DISPLAY_NAME_1 = "display_001"
TEST_DISPLAY_NAME_2 = "display_002"
TEST_MAP = "map_001"
TEST_MODE = "mode_001"

def test_payload() -> dict[str, object]:
    return {
        "weapon": "rifle",
        "damage": 34,
    }