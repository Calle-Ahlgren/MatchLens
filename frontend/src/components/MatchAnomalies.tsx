import { useEffect, useState } from 'react'
import { getMatchAnomalies, type AnomalyFlag } from '../api/anomalies'
import './MatchAnomalies.css'

type MatchAnomaliesProps = {
    matchId: string
}

function MatchAnomalies({ matchId }: MatchAnomaliesProps) {
    const [anomalies, setAnomalies] = useState<AnomalyFlag[]>([])

    const [isLoading, setIsLoading] = useState<boolean>(true)

    const [errorMsg, setErrorMsg] = useState<string | null>(null)
    
    useEffect(() => {
        async function loadAnomalies() {
            try {
                const anomalies = await getMatchAnomalies(matchId)

                setAnomalies(anomalies)

            } catch (error) {
                if(error instanceof Error) {
                    setErrorMsg('Failed to load anomalies: ' + error.message)
                } else {
                    setErrorMsg('An unexpected error occurred')
                }

            } finally {
                setIsLoading(false)
            }
        }

        loadAnomalies()
    }, [matchId])

    return (
        <div className="match-anomalies">
            {isLoading && <p>Loading anomalies</p>}
            
            {errorMsg !== null && <p>{errorMsg}</p>}

            {errorMsg === null && !isLoading && anomalies.length === 0 && (
                <p>No anomalies found</p>
            )}

            {!isLoading && errorMsg === null && anomalies.length > 0 && (
            <ul className="anomaly-list">
                {anomalies.map((anomaly, index) => (
                    <li key={index} className="anomaly-card">

                        <div className="anomaly-header">
                            <strong className="anomaly-type">
                                {anomaly.anomaly_type}
                            </strong>
                            <span className={`anomaly-severity severity-${anomaly.severity.toLowerCase()}`}>
                                {anomaly.severity}
                            </span>
                        </div>

                        <p className='anomaly-description'>{anomaly.description}</p>

                        <p className='anomaly-meta'>Player: {anomaly.player_id}</p>

                        {anomaly.event_id !== null && 
                            <p className='anomaly-meta'>Event: {anomaly.event_id}</p>}

                    </li>
                ))}
            </ul>
            )}
        </div>
        )
}

export default MatchAnomalies