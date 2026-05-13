export interface Event {
  id: string
  title: string
  description: string
  date: string
  time: string
  location: string
  type: 'irl' | 'online' | 'stream'
  tags: string[]
  rsvpUrl?: string
  discordEventUrl?: string
  rules?: string
  prize?: string
  active: boolean
}

export const events: Event[] = [
  {
    id: 'evt_001',
    title: 'IB6 Overwatch Night',
    description:
      'Weekly Overwatch 2 lobby. Stoner-friendly. Trash talk welcome. Skills optional.',
    date: '2026-05-17',
    time: '9:00 PM EST',
    location: 'Discord — IB6 Lobby',
    type: 'online',
    tags: ['ib6', 'gaming', 'weekly'],
    discordEventUrl: process.env.NEXT_PUBLIC_DISCORD_INVITE_URL,
    rules: 'Join the Discord. Be in the lobby by 9PM. Have fun.',
    prize: 'IB6 MVP badge + 50 points',
    active: true,
  },
  {
    id: 'evt_002',
    title: 'Cold Empire Pop-Up',
    description:
      'First official Cold Empire merch pop-up. Limited drops. Live music. Real ones only.',
    date: '2026-06-15',
    time: '2:00 PM – 8:00 PM',
    location: 'TBA — Check Discord for the drop',
    type: 'irl',
    tags: ['ccc', 'cartel', 'featured', 'irl'],
    rules: 'Free entry. Bring ID. Cold Empire gear encouraged.',
    prize: 'Exclusive pop-up only product',
    active: true,
  },
  {
    id: 'evt_003',
    title: 'Cold Cartel Initiation Stream',
    description:
      'Live Cartel briefing. Rank reveals. Mission drops. Watch for the clue.',
    date: '2026-05-25',
    time: '8:00 PM EST',
    location: 'Twitch / YouTube — links in Discord',
    type: 'stream',
    tags: ['cartel', 'stream', 'featured'],
    discordEventUrl: process.env.NEXT_PUBLIC_DISCORD_INVITE_URL,
    active: true,
  },
  {
    id: 'evt_004',
    title: 'IB6 Tournament — Round 1',
    description:
      'First official IB6 community tournament. Multiple games. Prizes. Chaos.',
    date: '2026-07-04',
    time: '12:00 PM EST',
    location: 'Discord — IB6 Tournament Stage',
    type: 'online',
    tags: ['ib6', 'gaming', 'tournament'],
    rules: '4-person teams. Register in Discord. Show up or forfeit.',
    prize: 'Custom IB6 merch pack + 500 points + champion badge',
    active: true,
  },
]

export function getEventById(id: string): Event | undefined {
  return events.find((e) => e.id === id)
}

export function getEventsByTag(tag: string): Event[] {
  return events.filter((e) => e.tags.includes(tag) && e.active)
}

export function getUpcomingEvents(): Event[] {
  const now = new Date()
  return events
    .filter((e) => e.active && new Date(e.date) >= now)
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
}
