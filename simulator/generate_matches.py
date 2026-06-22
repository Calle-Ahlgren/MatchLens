from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
import json


@dataclass(frozen=True)
class SimPlayer:
    player_id: str
    display_name: str


@dataclass(frozen=True)
class SimMatch:
    match_id: str
    started_at: datetime
    map_name: str
    game_mode: str


@dataclass(frozen=True)
class SimEvent:
    match_id: str
    event_type: str
    player_id: str | None
    timestamp: datetime
    payload: dict[str, Any]


def make_players(count: int) -> list[SimPlayer]:
    players = []

    for idx in range(count):
        player = SimPlayer(
            player_id=f"player_{idx + 1:03}",
            display_name=f"Player {idx + 1}",
        )
        players.append(player)

    return players


def make_match() -> SimMatch:
    match = SimMatch(
        match_id="match_001",
        started_at=datetime(2026, 1, 1, 1, 1, 1, tzinfo=UTC),
        map_name="Training Arena",
        game_mode="deathmatch",
    )

    return match


def make_events(match: SimMatch, players: list[SimPlayer]) -> list[SimEvent]:
    events = []

    for idx, player in enumerate(players):
        spawn_event = SimEvent(
            match_id=match.match_id,
            event_type="player_spawned",
            player_id=player.player_id,
            timestamp=match.started_at + timedelta(milliseconds=100),
            payload={"x": idx * 2, "y": 0},
        )

        move_event_1 = SimEvent(
            match_id=match.match_id,
            event_type="position_updated",
            player_id=player.player_id,
            timestamp=match.started_at + timedelta(milliseconds=100 * (idx + 1) * 2),
            payload={"x": idx * 2, "y": idx + 1},
        )

        move_event_2 = SimEvent(
            match_id=match.match_id,
            event_type="position_updated",
            player_id=player.player_id,
            timestamp=match.started_at + timedelta(milliseconds=110 * (idx + 1) * 2),
            payload={"x": idx * 2, "y": idx + 2},
        )

        events += [spawn_event, move_event_1, move_event_2]

    events.sort(key=lambda event: event.timestamp)
    return events


def main() -> None:
    players = make_players(4)

    match = make_match()

    events = make_events(match, players)

    output = {
        "match": asdict(match),
        "players": [asdict(player) for player in players],
        "events": [asdict(event) for event in events],
    }

    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
