from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
import json


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_PATH = OUTPUT_DIR / "sample_match.json"


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

    if len(players) >= 2:
        shot_event = SimEvent(
            match_id=match.match_id,
            event_type="shot_fired",
            player_id=players[0].player_id,
            timestamp=match.started_at + timedelta(milliseconds=1000),
            payload={
                "weapon": "rifle",
            },
        )

        hit_event = SimEvent(
            match_id=match.match_id,
            event_type="player_hit",
            player_id=players[0].player_id,
            timestamp=match.started_at + timedelta(milliseconds=1100),
            payload={
                "target_player_id": players[1].player_id,
                "damage": 100,
                "weapon": "rifle",
            },
        )

        death_event = SimEvent(
            match_id=match.match_id,
            event_type="player_death",
            player_id=players[1].player_id,
            timestamp=match.started_at + timedelta(milliseconds=1110),
            payload={
                "killer_player_id": players[0].player_id,
                "weapon": "rifle",
            },
        )

        kill_event = SimEvent(
            match_id=match.match_id,
            event_type="player_killed",
            player_id=players[0].player_id,
            timestamp=match.started_at + timedelta(milliseconds=1110),
            payload={
                "victim_player_id": players[1].player_id,
                "weapon": "rifle",
            },
        )

        events += [shot_event, hit_event, death_event, kill_event]

    events.sort(key=lambda event: event.timestamp)
    return events


def summarize_events(events: list[SimEvent]) -> dict[str, int]:
    event_summary = {}

    for event in events:
        event_summary[event.event_type] = event_summary.get(event.event_type, 0) + 1

    return event_summary


def write_match_data(output: dict[str, object]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    output_json = json.dumps(output, indent=2, default=str)
    OUTPUT_PATH.write_text(output_json, encoding="utf-8")


def main() -> None:
    players = make_players(4)

    match = make_match()

    events = make_events(match, players)

    event_summary = summarize_events(events)

    output = {
        "match": asdict(match),
        "players": [asdict(player) for player in players],
        "events": [asdict(event) for event in events],
        "event_summary": event_summary
    }

    write_match_data(output)

    print("Generated sample match data.")
    print(f"Output file: {OUTPUT_PATH}")
    print(f"Total events: {len(events)}")
    print("Event summary:")

    for event_type, count in event_summary.items():
        print(f"  {event_type}: {count}")


if __name__ == "__main__":
    main()
