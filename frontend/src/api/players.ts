export type Player = {
    player_id: string
    display_name: string
    created_at: string
}

export async function getMatchPlayers(
  matchId: string
): Promise<Player[]> {

    const response = await fetch(`/api/matches/${matchId}/players`)

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
    }

    const players: Player[] = await response.json()

    return players
}