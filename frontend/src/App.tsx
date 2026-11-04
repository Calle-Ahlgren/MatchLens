import { useEffect, useState } from 'react'
import { getMatches, type Match } from './api/matches'
import MatchCard from './components/MatchCard'
import './App.css'

function App() {  
    const appName = 'MatchLens'

    const [matches, setMatches] = useState<Match[]>([])

    const [isLoading, setIsLoading] = useState<boolean>(true)

    const [errorMsg, setErrorMsg] = useState<string | null>(null)

    const [selectMatchId, setSelectMatchId] = useState<string | null>(null)

    const [refreshCount, setRefreshCount] = useState<number>(0)

    useEffect(() => {
        async function loadMatches() {
            setIsLoading(true)
            setErrorMsg(null)
            try {
                const match_data: Match[] = await getMatches() 

                setMatches(match_data)

            } catch (error) {
                if(error instanceof Error) {
                setErrorMsg('Failed to load matches: ' + error.message)
                } else {
                setErrorMsg('An unexpected error occurred')
                }

            } finally {
                setIsLoading(false)
            }
        }

        loadMatches()
    }, [refreshCount])

    function handleSelectMatch(matchId: string) {
        if(matchId === selectMatchId) {
        setSelectMatchId(null)
        } else {
        setSelectMatchId(matchId)
        }
    }

    return (
        <main>
            <header className='dashboard-header'>
                <h1>{appName}</h1>
                <p>Multiplayer game telemetry analytics</p>
            </header>

            <section className="matches-section">
                <div className='matches-section-header'>
                    <h2>Matches</h2>
                    <button 
                        className='refresh-button'
                        disabled={isLoading}
                        onClick={() => {
                            setRefreshCount(previous => previous + 1)
                        }}
                    >
                        Refresh matches
                    </button>
                </div>
                
                {isLoading && <p>Loading matches</p>}
                
                {errorMsg !== null && <p>{errorMsg}</p>}

                {errorMsg === null && !isLoading && matches.length === 0 && (
                <p>No matches found</p>)}

                <ul className='match-list'>
                    {matches.map((match) => (
                        <MatchCard 
                            match={match} 
                            onSelect={handleSelectMatch} 
                            isSelected={match.match_id === selectMatchId} 
                            key={match.match_id}
                        />
                    ))}
                </ul>
            </section>
        </main>
    )
}

export default App