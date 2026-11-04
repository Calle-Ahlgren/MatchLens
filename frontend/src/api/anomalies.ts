export type AnomalyFlag = {
    match_id: string
    player_id: string
    event_id: string | null
    anomaly_type: string
    severity: string
    description: string
}

export async function getMatchAnomalies(
  matchId: string
): Promise<AnomalyFlag[]> {

    const response = await fetch(`/api/matches/${matchId}/anomalies`)

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
    }

    const anomalies: AnomalyFlag[] = await response.json()

    return anomalies
}