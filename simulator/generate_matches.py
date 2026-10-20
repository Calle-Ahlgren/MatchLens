from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
import json
import argparse


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_PATH = OUTPUT_DIR / "sample_match.json"


NORMAL = "normal"
IMPOSSIBLE_MOVEMENT = "impossible_movement"
HIGH_ACCURACY = "high_accuracy"
SUSPICIOUS_FIRE_RATE = "suspicious_fire_rate"


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
            player_id=f"player_{uuid.uuid4().hex[:8]}",
            display_name=f"Player {idx + 1}",
        )
        players.append(player)

    return players


def make_match() -> SimMatch:
    match = SimMatch(
        match_id=f"match_{uuid.uuid4().hex[:8]}",
        started_at=datetime(2026, 1, 1, 1, 1, 1, tzinfo=UTC),
        map_name="Training Arena",
        game_mode="deathmatch",
    )

    return match


def make_normal_events(match: SimMatch, players: list[SimPlayer]) -> list[SimEvent]:
    events = []

    for idx, player in enumerate(players):
        spawn_x = idx * 10
        spawn_y = 0
        spawn_event = SimEvent(
            match_id=match.match_id,
            event_type="player_spawned",
            player_id=player.player_id,
            timestamp=match.started_at + timedelta(milliseconds=100),
            payload={"x": spawn_x, "y": spawn_y},
        )

        move_event_1 = SimEvent(
            match_id=match.match_id,
            event_type="position_updated",
            player_id=player.player_id,
            timestamp=match.started_at + timedelta(seconds=1),
            payload={"x": spawn_x + 1, "y": spawn_y + 0.5},
        )

        move_event_2 = SimEvent(
            match_id=match.match_id,
            event_type="position_updated",
            player_id=player.player_id,
            timestamp=match.started_at + timedelta(seconds=2),
            payload={"x": spawn_x + 2, "y": spawn_y + 1.0},
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
                "x": 10,
                "y": 20,
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


def make_impossible_movement_events(
    match: SimMatch,
    players: list[SimPlayer],
) -> list[SimEvent]:
    events = []

    player = players[0].player_id

    events.append(
        SimEvent(
            match_id=match.match_id,
            event_type="position_updated",
            player_id=player,
            timestamp=match.started_at + timedelta(seconds=5),
            payload={"x": 0, "y": 0},
        )
    )

    events.append(
        SimEvent(
            match_id=match.match_id,
            event_type="position_updated",
            player_id=player,
            timestamp=match.started_at + timedelta(seconds=6),
            payload={"x": 30, "y": 40},
        )
    )

    events.sort(key=lambda event: event.timestamp)

    return events


def make_high_accuracy_events(
    match: SimMatch,
    players: list[SimPlayer],
) -> list[SimEvent]:
    events = []

    shot_count = 10
    hit_count = 9
    start_offset_seconds = 10

    shooter = players[0]
    target = players[1]

    for idx in range(shot_count):
        events.append(
            SimEvent(
                match_id=match.match_id,
                event_type="shot_fired",
                player_id=shooter.player_id,
                timestamp=match.started_at
                + timedelta(seconds=start_offset_seconds + idx),
                payload={"weapon": "rifle"},
            )
        )
        if idx < hit_count:
            events.append(
                SimEvent(
                    match_id=match.match_id,
                    event_type="player_hit",
                    player_id=shooter.player_id,
                    timestamp=match.started_at
                    + timedelta(seconds=start_offset_seconds + idx, microseconds=100),
                    payload={
                        "target_player_id": target.player_id,
                        "damage": 34,
                        "weapon": "rifle",
                    },
                )
            )

    events.sort(key=lambda event: event.timestamp)

    return events


def make_suspicious_fire_rate_events(
    match: SimMatch,
    players: list[SimPlayer],
) -> list[SimEvent]:
    events = []

    shooter = players[2]

    events.append(
        SimEvent(
            match_id=match.match_id,
            event_type="shot_fired",
            player_id=shooter.player_id,
            timestamp=match.started_at + timedelta(seconds=30),
            payload={"weapon": "rifle"},
        )
    )

    events.append(
        SimEvent(
            match_id=match.match_id,
            event_type="shot_fired",
            player_id=shooter.player_id,
            timestamp=match.started_at + timedelta(seconds=30, milliseconds=50),
            payload={"weapon": "rifle"},
        )
    )

    return events


def make_events(
    match: SimMatch,
    players: list[SimPlayer],
    scenarios: set[str] | None = None,
) -> list[SimEvent]:
    if scenarios is None:
        scenarios = {NORMAL}

    events = []

    if NORMAL in scenarios:
        events += make_normal_events(match, players)
    if IMPOSSIBLE_MOVEMENT in scenarios:
        events += make_impossible_movement_events(match, players)
    if HIGH_ACCURACY in scenarios:
        events += make_high_accuracy_events(match, players)
    if SUSPICIOUS_FIRE_RATE in scenarios:
        events += make_suspicious_fire_rate_events(match, players)
    
    return events


def generate_sample_match(
    scenarios: set[str],
) -> tuple[SimMatch, list[SimPlayer], list[SimEvent]]:
    players = make_players(4)
    
    match = make_match()
    
    events = make_events(match, players, scenarios)

    return players, match, events

def summarize_events(events: list[SimEvent]) -> dict[str, int]:
    event_summary = {}

    for event in events:
        event_summary[event.event_type] = event_summary.get(event.event_type, 0) + 1

    return event_summary


def datetime_to_api_string(value: datetime) -> str:
    return value.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def event_to_api_dict(event: SimEvent) -> dict[str, object]:
    event_dict = asdict(event)
    event_dict["timestamp"] = datetime_to_api_string(event.timestamp)
    return event_dict


def match_to_api_dict(match: SimMatch) -> dict[str, object]:
    match_dict = asdict(match)
    match_dict["started_at"] = datetime_to_api_string(match.started_at)
    return match_dict


def player_to_api_dict(player: SimPlayer) -> dict[str, object]:
    return asdict(player)


def write_match_data(output: dict[str, object]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    output_json = json.dumps(output, indent=2)
    OUTPUT_PATH.write_text(output_json, encoding="utf-8")


def parse_scenarios() -> set[str]:
    parser = argparse.ArgumentParser(
            description="Generate simulated multiplayer telemetry"
        )
    
    parser.add_argument(
        "--scenarios", 
        nargs="+",
        choices=[NORMAL, IMPOSSIBLE_MOVEMENT, HIGH_ACCURACY, SUSPICIOUS_FIRE_RATE],
        default=[NORMAL],
        help="Telemetry scenarios to generate (default: normal)")

    args = parser.parse_args()

    scenarios = set(args.scenarios)

    return scenarios


def main() -> None:
    scenarios = parse_scenarios()

    players, match, events = generate_sample_match(scenarios)

    event_summary = summarize_events(events)

    output = {
        "match": match_to_api_dict(match),
        "players": [player_to_api_dict(player) for player in players],
        "events": [event_to_api_dict(event) for event in events],
        "event_summary": event_summary,
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
