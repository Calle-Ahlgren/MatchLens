from generate_matches import (
    make_players,
    make_match,
    make_events,
    match_to_api_dict,
    player_to_api_dict,
    event_to_api_dict,
)

from api_client import post_json

def upload_sample_match() -> None:
    players = make_players(4)

    match = make_match()

    events = make_events(match, players)

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
    upload_sample_match()


if __name__ == "__main__":
    main()