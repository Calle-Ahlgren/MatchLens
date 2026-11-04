import { useEffect, useState } from 'react'
import { getMatchEvents, type TelemetryEvent } from '../api/events'
import './MatchEvents.css'

const EVENTS_PER_BATCH = 10

type MatchEventsProps = {
    matchId: string
}

function formatPayloadValue(value: unknown): string {
    if (typeof value === 'object' && value !== null) {
        return JSON.stringify(value)
    }

    return String(value)
}

function formatEventTimestamp(timestamp: string): string {
    return new Date(timestamp).toLocaleString(undefined, {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        fractionalSecondDigits: 3,
    })
}

function MatchEvents({ matchId }: MatchEventsProps) {
    const [events, setEvents] = useState<TelemetryEvent[]>([])

    const [isLoading, setIsLoading] = useState<boolean>(true)

    const [errorMsg, setErrorMsg] = useState<string | null>(null)

    const [selectedEventType, setSelectedEventType] = useState<string>('all')
    
    const [visibleCount, setVisibleCount] = useState<number>(EVENTS_PER_BATCH)

    useEffect(() => {
        async function loadEvents() {
        try {
            const events: TelemetryEvent[] = await getMatchEvents(matchId)

            setEvents(events)

        } catch (error) {
            if(error instanceof Error) {
                setErrorMsg('Failed to load events: ' + error.message)
            } else {
                setErrorMsg('An unexpected error occurred')
            }

        } finally {
            setIsLoading(false)
        }
        }

        loadEvents()
    }, [matchId])

    const eventTypes = [...new Set(events.map((event) => event.event_type))]

    const filteredEvents = 
        selectedEventType === 'all' ? 
        events : events.filter((event) => event.event_type === selectedEventType)

    const visibleEvents = filteredEvents.slice(0, visibleCount)

    return (
        <div>
            {isLoading && <p>Loading events</p>}
                
            {errorMsg !== null && <p>{errorMsg}</p>}

            {errorMsg === null && !isLoading && events.length === 0 && (
                <p>No events found</p>
            )}

            {!isLoading && errorMsg === null && events.length > 0 && (          
                <>
                <div className="event-filters">
                    <label htmlFor="event-type-filter">Event type</label>

                    <select
                        id="event-type-filter"
                        value={selectedEventType}
                        onChange={(event) => {
                            setSelectedEventType(event.target.value)
                            setVisibleCount(EVENTS_PER_BATCH)
                        }}
                    >
                        <option value="all">All event types</option>

                        {eventTypes.map((eventType) => (
                            <option key={eventType} value={eventType}>{eventType}</option>
                        ))}
                    </select>
                </div>

                <p className='event-count'>Showing {visibleEvents.length} of {filteredEvents.length} events</p>

                {filteredEvents.length === 0 && (
                    <p>No events match this filter.</p>
                )}

                {filteredEvents.length > 0 && (
                    <>
                    <ul className='event-list'>
                        {visibleEvents.map((event) => (
                            <li key={event.event_id} className="event-item">
                                <details>
                                    <summary className="event-summary">
                                        <strong>{event.event_type}</strong>
                                        <span className="event-timestamp">
                                            {formatEventTimestamp(event.timestamp)}
                                        </span>
                                    </summary>

                                    <div className="event-body">
                                        <strong>Event Details</strong>
                                        <p>Player: {event.player_id ?? 'N/A'}</p>
                                        <p>Event ID: {event.event_id}</p>
                                        {Object.entries(event.payload).map(([fieldName, value]) => (
                                            <p key={fieldName}>{fieldName}: {formatPayloadValue(value)}</p>
                                        ))}
                                    </div>
                                </details>
                            </li>
                        ))}
                    </ul>
                    {filteredEvents.length > visibleEvents.length && 
                        <button
                            type="button"
                            className='show-more-button'
                            onClick={() => {
                                setVisibleCount((previous) => previous + EVENTS_PER_BATCH)
                            }}
                        >
                            Show more events
                        </button>
                    }
                        
                    </>               
                )}
                
                </>
            )}
        </div>
    )
}

export default MatchEvents