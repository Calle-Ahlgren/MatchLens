export type TelemetryEvent = {
    event_id: string
    match_id: string
    event_type: string
    player_id: string | null
    timestamp: string
    payload: Record<string, unknown>
}

export async function getMatchEvents(
  matchId: string
): Promise<TelemetryEvent[]> {
    const response = await fetch(`/api/matches/${matchId}/events`)

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
    }

    const events: TelemetryEvent[] = await response.json()

    return events
}