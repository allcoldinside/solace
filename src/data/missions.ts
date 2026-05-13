export interface Mission {
  id: string
  title: string
  description: string
  objective: string
  reward: string
  points: number
  deadline?: string
  proofRequired: string
  proofType: 'text' | 'image' | 'link' | 'none'
  category: 'community' | 'purchase' | 'content' | 'event' | 'irl' | 'hidden'
  minRank: string
  active: boolean
}

export const missions: Mission[] = [
  {
    id: 'mission_find_qr',
    title: 'Find the QR',
    description: 'Locate a Cold Empire QR code in the wild and scan it.',
    objective: 'Find and scan a physical Cold Empire QR code.',
    reward: '50 points + Family Friend status',
    points: 50,
    proofRequired: 'Screenshot of the scanned code or the location where you found it.',
    proofType: 'image',
    category: 'irl',
    minRank: 'prospect',
    active: true,
  },
  {
    id: 'mission_read_code',
    title: 'Read the Cold Code',
    description: 'Read all 13 articles of the Cold Code.',
    objective: 'Read every article and submit your favorite quote.',
    reward: '75 points',
    points: 75,
    proofRequired: 'Your favorite quote from any article and why.',
    proofType: 'text',
    category: 'community',
    minRank: 'prospect',
    active: true,
  },
  {
    id: 'mission_wear_signal',
    title: 'Wear the Signal',
    description: 'Post a photo wearing Cold Empire gear in a public setting.',
    objective: 'Post publicly wearing CCC gear and submit the link.',
    reward: '100 points',
    points: 100,
    proofRequired: 'Link to your public post or photo of you wearing the gear.',
    proofType: 'link',
    category: 'content',
    minRank: 'family-friend',
    active: true,
  },
  {
    id: 'mission_refer_friend',
    title: 'Refer a Friend',
    description: 'Bring someone worthy into the empire.',
    objective: 'Refer a friend who signs up and completes their first mission.',
    reward: '150 points + referral credit',
    points: 150,
    proofRequired: 'The email or alias of the person you referred.',
    proofType: 'text',
    category: 'community',
    minRank: 'family-friend',
    active: true,
  },
  {
    id: 'mission_attend_game_night',
    title: 'Enter the Lobby',
    description: 'Attend an IB6 game night event.',
    objective: 'Join the Discord and participate in a scheduled game night.',
    reward: '125 points + IB6 Lobby badge',
    points: 125,
    proofRequired: 'Screenshot of you in the game night Discord channel.',
    proofType: 'image',
    category: 'event',
    minRank: 'family-friend',
    active: true,
  },
  {
    id: 'mission_first_drop',
    title: 'Buy a Drop',
    description: 'Make your first purchase from the Cold Empire store.',
    objective: 'Buy any product from the store.',
    reward: '200 points',
    points: 200,
    proofRequired: 'Auto-verified via order system.',
    proofType: 'none',
    category: 'purchase',
    minRank: 'family-friend',
    active: true,
  },
  {
    id: 'mission_decode_clue',
    title: 'Decode a Clue',
    description: 'Find and decode a hidden clue embedded in the Cold Empire site.',
    objective: 'Find a hidden message and submit what it says.',
    reward: '250 points + Clue Finder badge',
    points: 250,
    proofRequired: 'The decoded message.',
    proofType: 'text',
    category: 'hidden',
    minRank: 'associate',
    active: true,
  },
  {
    id: 'mission_attend_event',
    title: 'Show Up in Person',
    description: 'Attend a Cold Empire pop-up or real-world event.',
    objective: 'Attend any official Cold Empire IRL event.',
    reward: '300 points + Event Veteran badge',
    points: 300,
    proofRequired: 'Photo at the event.',
    proofType: 'image',
    category: 'event',
    minRank: 'associate',
    active: true,
  },
  {
    id: 'mission_creative',
    title: 'Build Something',
    description: 'Create original content inspired by the Cold Empire.',
    objective: 'Submit original art, music, video, or writing connected to the brand.',
    reward: '350 points + Creator badge',
    points: 350,
    proofRequired: 'Link to or file of your creation.',
    proofType: 'link',
    category: 'content',
    minRank: 'associate',
    active: true,
  },
  {
    id: 'mission_ten_missions',
    title: 'The Long Game',
    description: 'Complete 10 missions total.',
    objective: 'Accumulate 10 mission completions across any categories.',
    reward: '500 points + Lieutenant consideration',
    points: 500,
    proofRequired: 'Auto-verified when milestone is reached.',
    proofType: 'none',
    category: 'community',
    minRank: 'associate',
    active: true,
  },
]

export function getMissionById(id: string): Mission | undefined {
  return missions.find((m) => m.id === id)
}

export function getActiveMissions(): Mission[] {
  return missions.filter((m) => m.active)
}

export function getMissionsByRank(rankId: string): Mission[] {
  const rankOrder = ['prospect', 'family-friend', 'associate', 'lieutenant', 'capo', 'don', 'boss']
  const userLevel = rankOrder.indexOf(rankId)
  return missions.filter((m) => {
    const missionLevel = rankOrder.indexOf(m.minRank)
    return missionLevel <= userLevel && m.active
  })
}
