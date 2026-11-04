export type PlayerMatchStats = {
    match_id: string
    player_id: string
    shots_fired: number
    hits: number
    kills: number
    deaths: number
    accuracy: number
}

export async function getPlayerMatchStats(
  matchId: string,
  playerId: string
): Promise<PlayerMatchStats> {

    const response = await fetch(`/api/matches/${matchId}/players/${playerId}/stats`)

    if(!response.ok) {
        throw new Error(`HTTP ${response.status}`)
    }

    const playerMatchStats: PlayerMatchStats = await response.json()

    return playerMatchStats
}