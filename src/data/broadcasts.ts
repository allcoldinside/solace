export interface Episode {
  id: string
  slug: string
  title: string
  number: number
  series: string
  description: string
  duration: string
  date: string
  spotifyUrl?: string
  youtubeUrl?: string
  keyQuotes: string[]
  relatedCodeSlug?: string
  relatedProductSlug?: string
  tags: string[]
}

export const episodes: Episode[] = [
  {
    id: 'ep_001',
    slug: 'you-dont-know-me-but-youre-going-to',
    title: "You Don't Know Me, But You're Going To",
    number: 1,
    series: "Cold's Corner",
    description:
      "The first transmission. Who is Cold Empire, why does it exist, and what are we actually building here. An honest conversation about building something real from nothing.",
    duration: '42 min',
    date: '2026-04-01',
    keyQuotes: [
      '"Most brands want to be known. We want to be found."',
      '"The door is a filter. Not everyone should walk through it."',
      '"We are not building a company. We are building a territory."',
    ],
    relatedCodeSlug: 'the-door-is-earned',
    relatedProductSlug: 'find-the-door-hoodie',
    tags: ['cold-corner', 'brand', 'featured'],
  },
  {
    id: 'ep_002',
    slug: 'the-cartel-explained',
    title: 'The Cartel Explained',
    number: 2,
    series: 'Cartel Transmissions',
    description:
      'What is Cold Cartel, why does it exist, how does membership work, and what does rank actually mean inside the empire. All questions answered in one transmission.',
    duration: '38 min',
    date: '2026-04-08',
    keyQuotes: [
      '"Rank is not a title. It is a responsibility."',
      '"Before rank comes code. Before code comes curiosity."',
      '"Every member of this empire was once a stranger at the door."',
    ],
    relatedCodeSlug: 'loyalty-builds-the-room',
    relatedProductSlug: 'cartel-blackout-hat',
    tags: ['cartel-transmissions', 'cartel', 'featured'],
  },
  {
    id: 'ep_003',
    slug: 'ib6-the-gaming-wing',
    title: 'IB6 — The Gaming Wing',
    number: 3,
    series: 'IB6 Lobby Talk',
    description:
      'Ice Bong Six exists because stoner gamers deserve a home that does not take itself too seriously. Table talk about building a genuine gaming community.',
    duration: '35 min',
    date: '2026-04-15',
    keyQuotes: [
      '"For the fkn fun of it. That\'s the whole mission."',
      '"We don\'t care about your KD. We care about your vibe."',
      '"The lobby is the community. Protect the lobby."',
    ],
    relatedCodeSlug: 'respect-the-lobby',
    relatedProductSlug: 'ib6-lobby-hoodie',
    tags: ['ib6-lobby-talk', 'ib6', 'gaming'],
  },
  {
    id: 'ep_004',
    slug: 'building-a-brand-from-a-sticker',
    title: 'Building a Brand From a Sticker',
    number: 4,
    series: "Cold's Corner",
    description:
      'How does a brand grow from a QR code on a sticker to a full empire? The mechanics of building organic attention without a budget.',
    duration: '51 min',
    date: '2026-04-22',
    keyQuotes: [
      '"Every sticker is a door. Some people find it. Most walk past it."',
      '"The best marketing is a mystery."',
      '"We never told people what to think. We showed them where to look."',
    ],
    relatedCodeSlug: 'move-quiet-hit-loud',
    relatedProductSlug: 'no-fake-smoke-sticker-pack',
    tags: ['cold-corner', 'brand', 'strategy'],
  },
]

export function getEpisodeBySlug(slug: string): Episode | undefined {
  return episodes.find((e) => e.slug === slug)
}

export function getEpisodesByTag(tag: string): Episode[] {
  return episodes.filter((e) => e.tags.includes(tag))
}

export const series = [
  { id: 'cold-corner', name: "Cold's Corner", description: 'Brand, strategy, and the real talk.' },
  { id: 'cartel-transmissions', name: 'Cartel Transmissions', description: 'Membership, rank, and the inner layer.' },
  { id: 'ib6-lobby-talk', name: 'IB6 Lobby Talk', description: 'Gaming, community, and the chaos.' },
  { id: 'behind-the-door', name: 'Behind the Door', description: 'Behind-the-scenes of building the empire.' },
]
