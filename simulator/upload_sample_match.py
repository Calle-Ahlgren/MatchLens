from generate_matches import (
    generate_sample_match,
    match_to_api_dict,
    player_to_api_dict,
    event_to_api_dict,
    parse_scenarios,    
)

from api_client import post_json


def upload_sample_match(scenarios: set[str]) -> None:
    players, match, events = generate_sample_match(scenarios)

    match_dict = match_to_api_dict(match)

    match_entry = post_json("/matches", match_dict)

    for player in players:
        player_dict = player_to_api_dict(player)
        post_json("/players", player_dict)

    for event in events:
        event_dict = event_to_api_dict(event)
        post_json("/events", event_dict)

    print(f"Uploaded match: {match_entry['match_id']}")
    print(f"Uploaded players: {len(players)}")
    print(f"Uploaded events: {len(events)}")


def main() -> None:
    scenarios = parse_scenarios()

    upload_sample_match(scenarios)


if __name__ == "__main__":
    main()
