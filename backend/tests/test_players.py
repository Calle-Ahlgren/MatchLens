import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.players import create_player
from app.schemas.players import PlayerCreate
from tests.db_test_utils import clear_database_tables, create_test_player
import sample_data as data


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_test_database() -> None:
    clear_database_tables()

    yield

    clear_database_tables()


def test_create_player_accepts_valid_player() -> None:
    player = {
        "player_id": data.TEST_PLAYER_ID_1,
        "display_name": data.TEST_DISPLAY_NAME_1,
    }

    response = client.post("/players", json=player)
    response_json = response.json()

    assert response.status_code == 200

    assert response_json["player_id"] == data.TEST_PLAYER_ID_1
    assert response_json["display_name"] == data.TEST_DISPLAY_NAME_1
    assert response_json["created_at"]


def test_get_player_by_id_returns_created_player() -> None:
    create_test_player()

    response = client.get(f"/players/{data.TEST_PLAYER_ID_1}")

    assert response.status_code == 200

    player = response.json()

    assert player["player_id"] == data.TEST_PLAYER_ID_1
    assert player["display_name"] == data.TEST_DISPLAY_NAME_1


def test_get_player_by_id_returns_404_for_unknown_player() -> None:
    response = client.get("/players/not_a_player")

    assert response.status_code == 404

    assert response.json()["detail"] == "Player not found"


def test_list_players_returns_created_players() -> None:
    create_test_player()
    create_player(
        PlayerCreate(
            player_id=data.TEST_PLAYER_ID_2,
            display_name=data.TEST_DISPLAY_NAME_2
        )
    )

    response = client.get("/players")
    players = response.json()

    assert response.status_code == 200
    assert len(players) == 2

    assert players[0]["player_id"] == data.TEST_PLAYER_ID_1
    assert players[0]["display_name"] == data.TEST_DISPLAY_NAME_1
    assert players[0]["created_at"]

    assert players[1]["player_id"] == data.TEST_PLAYER_ID_2
    assert players[1]["display_name"] == data.TEST_DISPLAY_NAME_2
    assert players[1]["created_at"]