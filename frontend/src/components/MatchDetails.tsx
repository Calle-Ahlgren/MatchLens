import { useState } from 'react'
import MatchEvents from './MatchEvents'
import MatchPlayers from './MatchPlayers'
import MatchAnomalies from './MatchAnomalies'
import './MatchDetails.css'

type MatchDetailsProps = {
    matchId: string
}

function MatchDetails({ matchId }: MatchDetailsProps) {
    const [hasOpenedEvents, setHasOpenedEvents] = useState<boolean>(false)
    const [hasOpenedPlayers, setHasOpenedPlayers] = useState<boolean>(false)
    const [hasOpenedAnomalies, setHasOpenedAnomalies] = useState<boolean>(false)

    return (
        <div className="match-details">
            <details
                onToggle={(event) => {
                    if(event.currentTarget.open) {
                        setHasOpenedPlayers(true)
                    }
                }}
            >
                <summary>Players</summary>

                {hasOpenedPlayers && <MatchPlayers matchId={matchId}/>}
            </details>
            <details
                onToggle={(event) => {
                    if(event.currentTarget.open) {
                        setHasOpenedEvents(true)
                    }
                }}
            >
                <summary>Events</summary>

                {hasOpenedEvents && <MatchEvents matchId={matchId}/>}
            </details>
            <details
                onToggle={(event) => {
                    if(event.currentTarget.open) {
                        setHasOpenedAnomalies(true)
                    }
                }}
            >
                <summary>Anomalies</summary>

                {hasOpenedAnomalies && <MatchAnomalies matchId={matchId}/>}
            </details>
        </div>
    )
}

export default MatchDetails