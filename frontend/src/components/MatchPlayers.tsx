import { useEffect, useState } from 'react'
import { getMatchPlayers, type Player } from '../api/players'
import PlayerStats from './PlayerStats'
import './MatchPlayers.css'

type MatchPlayersProps = {
    matchId: string
}

function MatchPlayers({ matchId }: MatchPlayersProps) {
    const [players, setPlayers] = useState<Player[]>([])

    const [isLoading, setIsLoading] = useState<boolean>(true)

    const [errorMsg, setErrorMsg] = useState<string | null>(null)

    useEffect(() => {
        async function loadPlayers() {
        try {
            const players: Player[] = await getMatchPlayers(matchId)

            setPlayers(players)
            
        } catch(error) {
            if(error instanceof Error) {
            setErrorMsg('Failed to load players: ' + error.message)
            } else {
            setErrorMsg('An unexpected error occurred')
            }

        } finally {
            setIsLoading(false)
        }
        }

        loadPlayers()
    }, [matchId])

    return (
        <div>
            {isLoading && <p>Loading players...</p>}
                
            {errorMsg !== null && <p>{errorMsg}</p>}

            {errorMsg === null && !isLoading && players.length === 0 && (
                <p>No players found</p>
            )}

            {!isLoading && errorMsg === null && players.length > 0 && (
                <ul className='player-list'>
                    {players.map((player) => (
                        <PlayerStats matchId={matchId} player={player} key={player.player_id}/>
                    ))}
                </ul>
            )}
        </div>
    )
}

export default MatchPlayers