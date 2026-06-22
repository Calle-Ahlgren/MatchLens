# MatchLens Event Contract

This document defines the current telemetry event types used by MatchLens.

The goal is to keep the simulator, backend API, database, analytics code, and future dashboard aligned on what each event means.

## General rule

Each telemetry event has a top-level `player_id`.

In the current MatchLens design:

```text
event.player_id = the player whose event stream this event belongs to
```

For player statistics, MatchLens currently counts events by selecting events for a specific `match_id` and `player_id`.

The `payload` field contains event-specific details. It is stored as flexible JSON for now. Payload validation is planned as future work, after the event contract has stabilized.

## Current event types

| Event type         | Owner          | Meaning                                  |
| ------------------ | -------------- | ---------------------------------------- |
| `player_spawned`   | spawned player | A player spawned into the match          |
| `position_updated` | moved player   | A player's position changed              |
| `shot_fired`       | shooter        | A player fired a shot                    |
| `player_hit`       | attacker       | A player successfully hit another player |
| `player_killed`    | killer         | A player killed another player           |
| `player_death`     | victim         | A player died                            |

## Event details

### `player_spawned`

A player spawned into the match.

Owner:

```text
player_id = spawned player
```

Required payload fields:

```text
x: number
y: number
```

Optional payload fields:

```text
z: number
team_id: string
spawn_point_id: string
```

Stats impact:

```text
None currently.
```

Example:

```json
{
  "match_id": "match_001",
  "event_type": "player_spawned",
  "player_id": "player_001",
  "timestamp": "2026-01-01T01:01:01Z",
  "payload": {
    "x": 0,
    "y": 0
  }
}
```

---

### `position_updated`

A player's position changed during the match.

Owner:

```text
player_id = moved player
```

Required payload fields:

```text
x: number
y: number
```

Optional payload fields:

```text
z: number
speed: number
direction: string
```

Stats impact:

```text
None currently.

Later, position events may be used for movement-based anomaly detection, such as impossible movement speed.
```

Example:

```json
{
  "match_id": "match_001",
  "event_type": "position_updated",
  "player_id": "player_001",
  "timestamp": "2026-01-01T01:01:02Z",
  "payload": {
    "x": 4,
    "y": 2
  }
}
```

---

### `shot_fired`

A player fired a shot.

A shot does not require a victim. Shots can miss, be fired at the environment, or have no known target.

Owner:

```text
player_id = shooter
```

Required payload fields:

```text
weapon: string
```

Optional payload fields:

```text
intended_target_player_id: string
ammo_before: number
ammo_after: number
```

Stats impact:

```text
shots_fired +1 for the owner
```

Example:

```json
{
  "match_id": "match_001",
  "event_type": "shot_fired",
  "player_id": "player_001",
  "timestamp": "2026-01-01T01:01:03Z",
  "payload": {
    "weapon": "rifle"
  }
}
```

---

### `player_hit`

A player successfully hit another player.

This is attacker-owned. The victim is stored in the payload.

Owner:

```text
player_id = attacker
```

Required payload fields:

```text
target_player_id: string
damage: number
weapon: string
```

Optional payload fields:

```text
hit_location: string
distance: number
```

Stats impact:

```text
hits +1 for the owner
```

Example:

```json
{
  "match_id": "match_001",
  "event_type": "player_hit",
  "player_id": "player_001",
  "timestamp": "2026-01-01T01:01:04Z",
  "payload": {
    "target_player_id": "player_002",
    "damage": 100,
    "weapon": "rifle"
  }
}
```

---

### `player_killed`

A player killed another player.

This is killer-owned. The victim is stored in the payload.

Owner:

```text
player_id = killer
```

Required payload fields:

```text
victim_player_id: string
weapon: string
```

Optional payload fields:

```text
damage: number
headshot: boolean
```

Stats impact:

```text
kills +1 for the owner
```

Example:

```json
{
  "match_id": "match_001",
  "event_type": "player_killed",
  "player_id": "player_001",
  "timestamp": "2026-01-01T01:01:05Z",
  "payload": {
    "victim_player_id": "player_002",
    "weapon": "rifle"
  }
}
```

---

### `player_death`

A player died.

This is victim-owned. The killer, if known, is stored in the payload.

Owner:

```text
player_id = victim
```

Required payload fields:

```text
killer_player_id: string
weapon: string
```

Optional payload fields:

```text
damage: number
death_cause: string
```

Stats impact:

```text
deaths +1 for the owner
```

Example:

```json
{
  "match_id": "match_001",
  "event_type": "player_death",
  "player_id": "player_002",
  "timestamp": "2026-01-01T01:01:05Z",
  "payload": {
    "killer_player_id": "player_001",
    "weapon": "rifle"
  }
}
```

## Kill/death event pair

A single elimination may produce both:

```text
player_killed
player_death
```

These represent the same outcome from two different player streams.

Example:

```text
player_001 kills player_002
```

This creates:

```text
player_killed
  owner: player_001
  stats impact: player_001 kills +1

player_death
  owner: player_002
  stats impact: player_002 deaths +1
```

This duplication is intentional in the current design because player-scoped stats are computed from each player's own event stream.

## Current limitations

Payloads are currently stored as flexible JSON.

The backend validates the top-level event structure and event type, but it does not yet validate event-type-specific payload fields.

For example, the backend currently accepts a `player_hit` event even if its payload is missing `target_player_id`.

This is acceptable during the early simulator phase, but payload validation should be added later.

## Future payload validation

Possible future validation approach:

```text
shot_fired requires:
  weapon

player_hit requires:
  target_player_id
  damage
  weapon

player_killed requires:
  victim_player_id
  weapon

player_death requires:
  killer_player_id
  weapon
```

This could be implemented with either:

```text
manual validation based on event_type
```

or:

```text
separate Pydantic payload models per event type
```

Manual validation is probably enough for the MVP.

## Possible future event types

### `player_damaged`

A victim-owned event representing damage taken.

This is not currently part of the MVP.

Possible meaning:

```text
player_id = damaged player
```

Possible payload:

```json
{
  "attacker_player_id": "player_001",
  "damage": 34,
  "weapon": "rifle"
}
```

This could support future stats such as:

```text
damage_taken
hits_taken
damage_dealt
```

For now, MatchLens only tracks `player_hit` from the attacker's perspective.
