import { useEffect, useState } from 'react'
import { getPlayerMatchStats, type PlayerMatchStats } from '../api/playerStats'
import type { Player } from '../api/players'
import './PlayerStats.css'

type PlayerStatsProps = {
    matchId: string
    player: Player
}

function PlayerStats({ matchId, player }: PlayerStatsProps) {
    const [hasOpened, setHasOpened] = useState<boolean>(false)
    const [stats, setStats] = useState<PlayerMatchStats | null>(null)
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [errorMsg, setErrorMsg] = useState<string | null>(null)

    useEffect(() => {
        if (!hasOpened) {
            return
        }

        async function loadStats() {
        setIsLoading(true)

        try {
            const playerStats: PlayerMatchStats = await getPlayerMatchStats(matchId, player.player_id)
            setStats(playerStats)

        } catch(error) {
            if(error instanceof Error) {
            setErrorMsg('Failed to load player statistics: ' + error.message)
            } else {
            setErrorMsg('An unexpected error occurred')
            }
        } finally {
            setIsLoading(false)
        }
        }

        loadStats()
        }, [hasOpened, matchId, player.player_id])

    return (
        <li className='list-item'>
            <details
                onToggle={(event) => {
                if (event.currentTarget.open) {
                    setHasOpened(true)
                }
                }}
            >
                <summary className="player-summary">
                    <strong>{player.display_name}</strong>
                    <span className="player-id">{player.player_id}</span>
                </summary>

                {isLoading && <p>Loading player statistics...</p>}

                {errorMsg !== null && <p>{errorMsg}</p>}

                {stats !== null && (
                <div className="player-stats-grid">

                    <div className="stat-item">
                        <strong>{stats.kills}</strong>
                        <span>Kills</span>
                    </div>

                    <div className="stat-item">
                        <strong>{stats.deaths}</strong>
                        <span>Deaths</span>
                    </div>

                    <div className="stat-item">
                        <strong>{stats.shots_fired}</strong>
                        <span>Shots fired</span>
                    </div>

                    <div className="stat-item">
                        <strong>{stats.hits}</strong>
                        <span>Hits</span>
                    </div>

                    <div className="stat-item">
                        <strong>
                            {new Intl.NumberFormat(undefined, {
                            style: 'percent',
                            maximumFractionDigits: 1,
                            }).format(stats.accuracy)}
                        </strong>
                        <span>Accuracy</span>
                    </div>
                </div>
                )}
            </details>
        </li>
    )
}

export default PlayerStats