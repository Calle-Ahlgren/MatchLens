import type { Match } from '../api/matches'
import MatchDetails from './MatchDetails'
import './MatchCard.css'

type MatchCardProps = {
    match: Match
    onSelect: (matchId: string) => void
    isSelected: boolean
}

function MatchCard({match, onSelect, isSelected}: MatchCardProps) {
    return (
        <li className='match-card'>
            <div className='match-card-header'>
                <h3>{match.map_name}</h3>
                <p>{match.game_mode}</p>
            </div>
            <p>{new Date(match.started_at).toLocaleString()}</p>
            <p>{match.match_id}</p>
            <button className='details-button' onClick={() => onSelect(match.match_id)}>
                {isSelected ? 'Hide details' : 'View details'}
            </button>
            {isSelected && <MatchDetails matchId={match.match_id}/>}
        </li>
  )
}

export default MatchCard