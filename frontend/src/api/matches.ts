export type Match = {
    match_id: string
    started_at: string
    map_name: string
    game_mode: string
}

export async function getMatches(): Promise<Match[]> {
    const response = await fetch('/api/matches')
    
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
    }

    const match_data: Match[] = await response.json()

    return match_data
}