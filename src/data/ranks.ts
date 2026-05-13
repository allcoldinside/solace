export interface Rank {
  id: string
  name: string
  level: number
  description: string
  perks: string[]
  requirements: string
  pointsRequired: number
  color: string
}

export const ranks: Rank[] = [
  {
    id: 'family-friend',
    name: 'Family Friend',
    level: 1,
    description:
      'You found the door. You stepped inside. You are recognized as someone who belongs here.',
    perks: [
      'Access to public Cold Code',
      'Community Discord access',
      'Drop alerts',
      'Event invitations',
    ],
    requirements: 'Join the community and verify your email.',
    pointsRequired: 0,
    color: '#888888',
  },
  {
    id: 'associate',
    name: 'Associate',
    level: 2,
    description:
      'First real step inside. You have shown you understand the code and you are willing to contribute.',
    perks: [
      'All Family Friend perks',
      'Entry-level mission access',
      'Associate-only Discord channels',
      'Early drop notifications',
      '10% store discount',
    ],
    requirements: 'Complete 3 missions and accumulate 100 points.',
    pointsRequired: 100,
    color: '#c9a84c',
  },
  {
    id: 'lieutenant',
    name: 'Lieutenant',
    level: 3,
    description:
      'You have proven consistency. You show up. You contribute. The crew recognizes you.',
    perks: [
      'All Associate perks',
      'Lieutenant mission access',
      'Early access to drops (48 hours)',
      '15% store discount',
      'Vote on community decisions',
      'Exclusive Lieutenant content',
    ],
    requirements: 'Complete 10 missions and accumulate 500 points.',
    pointsRequired: 500,
    color: '#00cc33',
  },
  {
    id: 'capo',
    name: 'Capo',
    level: 4,
    description:
      'You help run the room. Leaders know your name. Your actions shape the community.',
    perks: [
      'All Lieutenant perks',
      'Capo mission access',
      'Exclusive Capo merch drops',
      '20% store discount',
      'Event planning access',
      'Community moderation tools',
      'Private Capo briefings',
    ],
    requirements: 'Complete 25 missions, attend 3 events, and accumulate 1,500 points.',
    pointsRequired: 1500,
    color: '#00ff41',
  },
  {
    id: 'don',
    name: 'Don',
    level: 5,
    description:
      'The room defers to you. You have built something inside the empire that the empire runs on.',
    perks: [
      'All Capo perks',
      'Don-level access to all content',
      'First access to all drops',
      '25% store discount',
      'Co-branding opportunity',
      'Revenue share on referred sales',
      'Private Don communication line',
    ],
    requirements: 'Complete 50 missions, attend 5 events, accumulate 5,000 points, and be nominated by existing Dons.',
    pointsRequired: 5000,
    color: '#c9a84c',
  },
  {
    id: 'boss',
    name: 'Boss',
    level: 6,
    description:
      'You helped build the empire. Not just participate in it. The empire carries your fingerprints.',
    perks: [
      'All Don perks',
      'Equity conversation eligibility',
      'Custom Cold Empire product collab',
      'Permanent 30% store discount',
      'Boss-tier exclusive events',
      'Empire strategy table seat',
      'Legacy recognition',
    ],
    requirements: 'By invitation only. Reserved for those who have demonstrably shaped the empire.',
    pointsRequired: 10000,
    color: '#ff2222',
  },
]

export function getRankById(id: string): Rank | undefined {
  return ranks.find((r) => r.id === id)
}

export function getNextRank(currentRankId: string): Rank | undefined {
  const current = ranks.find((r) => r.id === currentRankId)
  if (!current) return undefined
  return ranks.find((r) => r.level === current.level + 1)
}
