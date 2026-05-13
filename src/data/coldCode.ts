export interface ColdCodeArticle {
  id: number
  slug: string
  title: string
  shortTitle: string
  teaser: string
  rule: string
  meaning: string
  looksLike: string
  breaksIt: string
  whyItMatters: string
  relatedMission: string
  relatedProduct: string
  relatedRank: string
}

export const coldCodeArticles: ColdCodeArticle[] = [
  {
    id: 1,
    slug: 'the-door-is-earned',
    title: 'Article I — The Door Is Earned',
    shortTitle: 'The Door Is Earned',
    teaser: 'Not everyone finds the door. Not everyone who finds it deserves to walk through.',
    rule: 'The door is earned, not given.',
    meaning:
      'Access to the Cold Empire is not something you stumble into and take. It is something you move toward with intention. You find the door because you were looking. You get in because you put in the work.',
    looksLike:
      'Showing up to events. Completing missions. Wearing the signal. Reading the code. Engaging with the community before asking what you get out of it.',
    breaksIt:
      'Expecting rank without effort. Showing up only when there is something to take. Skipping the code and demanding access anyway.',
    whyItMatters:
      'Every room in this empire is built by people who showed up. If the door were free, the room would be empty. The filter keeps the signal clean.',
    relatedMission: 'Find the QR',
    relatedProduct: 'Find the Door Hoodie',
    relatedRank: 'Family Friend',
  },
  {
    id: 2,
    slug: 'loyalty-builds-the-room',
    title: 'Article II — Loyalty Builds the Room',
    shortTitle: 'Loyalty Builds the Room',
    teaser: 'The room is only as strong as the people inside it. Loyalty is the foundation.',
    rule: 'You do not eat what you did not help build.',
    meaning:
      'Loyalty is not blind. It is chosen. When you are loyal to the Cold Empire, you are loyal to every person who showed up before you and every person who will come after. You protect the room.',
    looksLike:
      'Inviting people in who deserve it. Vouching for your crew. Not talking about what happens inside when you are outside. Showing up when it is inconvenient.',
    breaksIt:
      'Taking credit for others\' work. Leaving when things get difficult. Sharing insider information without permission. Putting yourself above the crew.',
    whyItMatters:
      'Trust is the currency of this empire. Without it, nothing holds. Every deal, every drop, every rank up runs on trust. Loyalty protects it.',
    relatedMission: 'Refer a Friend',
    relatedProduct: 'Family Friend Hoodie',
    relatedRank: 'Associate',
  },
  {
    id: 3,
    slug: 'the-signal-must-stay-clean',
    title: 'Article III — The Signal Must Stay Clean',
    shortTitle: 'The Signal Must Stay Clean',
    teaser: 'The brand is the territory. Noise corrupts signal. Keep it clean.',
    rule: 'What you put out in the name of Cold Empire is Cold Empire.',
    meaning:
      'When you wear the brand, post with the brand, or speak on behalf of the community, you are the signal. A dirty signal confuses people, dilutes the message, and weakens the territory.',
    looksLike:
      'Representing the brand with accuracy. Not over-explaining. Not watering down the identity to appeal to people who do not get it. Keeping your content aligned with what the empire stands for.',
    breaksIt:
      'Posting low-quality content with our branding. Making promises the empire cannot keep. Misrepresenting the rank structure or the code. Clout chasing with the name.',
    whyItMatters:
      'The signal is how people find the door. If the signal is corrupted, the right people never arrive. The wrong ones do.',
    relatedMission: 'Post Wearing the Signal',
    relatedProduct: 'Cold Signal Tee',
    relatedRank: 'Lieutenant',
  },
  {
    id: 4,
    slug: 'family-eats-before-fame',
    title: 'Article IV — Family Eats Before Fame',
    shortTitle: 'Family Eats Before Fame',
    teaser: 'The crew that built it eats first. Fame is noise. Family is structure.',
    rule: 'Take care of the people who take care of you, before you take care of your image.',
    meaning:
      'Every empire is built by people who were there before there was anything to be proud of. Those people eat first. Fame is a consequence of the work, not the goal of it.',
    looksLike:
      'Crediting collaborators. Paying people properly. Shouting out the crew before you shout out yourself. Making sure the people closest to the build are rewarded before outside attention arrives.',
    breaksIt:
      'Using the platform for personal fame while the people who built it get nothing. Taking the interview and not mentioning the crew. Letting outside attention change how you treat the inner circle.',
    whyItMatters:
      'If the crew feels used, they leave. If they leave, the empire hollows out. The foundation is people, not followers.',
    relatedMission: 'Attend a Community Event',
    relatedProduct: 'Cartel Crew Hoodie',
    relatedRank: 'Capo',
  },
  {
    id: 5,
    slug: 'no-fake-smoke',
    title: 'Article V — No Fake Smoke',
    shortTitle: 'No Fake Smoke',
    teaser: 'Real is the only currency that holds value here. Faking it costs everyone.',
    rule: 'Do not fake it. Do not front it. Do not force it.',
    meaning:
      'Authenticity is not a trend in this empire. It is a requirement. Fake smoke means fake product, fake energy, fake community, fake loyalty. Everything built on it collapses.',
    looksLike:
      'Selling what you actually have. Saying what you actually mean. Showing up as yourself, not a character. Admitting when you do not know something.',
    breaksIt:
      'Overselling products you cannot deliver. Pretending to have access or rank you do not have. Performing community without actually being part of it. Faking content for metrics.',
    whyItMatters:
      'People can smell fake smoke. It pushes the right people away and attracts the wrong ones. The empire runs on real.',
    relatedMission: 'Submit a Real Review',
    relatedProduct: 'No Fake Smoke Sticker Pack',
    relatedRank: 'Associate',
  },
  {
    id: 6,
    slug: 'respect-the-lobby',
    title: 'Article VI — Respect the Lobby',
    shortTitle: 'Respect the Lobby',
    teaser: 'The lobby is where the community lives. Trash the lobby and you trash the home.',
    rule: 'The lobby is shared space. Treat it accordingly.',
    meaning:
      'The lobby — Discord, events, stream chat, community spaces — is where the empire exists in real time. How you act in the lobby reflects on every member. The lobby is the empire\'s living room.',
    looksLike:
      'Keeping it constructive. Welcoming newcomers. Not dominating the space. Calling out toxicity without becoming it. Keeping the community focused on what the empire is about.',
    breaksIt:
      'Drama for no reason. Talking over others. Gatekeeping without authority. Being toxic in game nights. Turning community space into personal space.',
    whyItMatters:
      'A good lobby keeps people coming back. A toxic one empties the room. The lobby is recruitment. Keep it somewhere people want to be.',
    relatedMission: 'Attend a Game Night',
    relatedProduct: 'IB6 Lobby Hoodie',
    relatedRank: 'Family Friend',
  },
  {
    id: 7,
    slug: 'build-more-than-you-brag',
    title: 'Article VII — Build More Than You Brag',
    shortTitle: 'Build More Than You Brag',
    teaser: 'The loudest people in the room are rarely the ones doing the work.',
    rule: 'Let the work speak first. Your mouth second.',
    meaning:
      'Building means actual output — products, content, community contributions, events, missions. Bragging means posting about what you plan to do. The empire values builders over talkers.',
    looksLike:
      'Finishing things before announcing them. Delivering before promoting. Letting your rank be visible through your actions, not your claims.',
    breaksIt:
      'Announcing projects that never ship. Claiming credit before the work is done. Treating rank like a badge to show off rather than a responsibility to carry.',
    whyItMatters:
      'Talk is free. In a noisy world, people respect action. The empire is built on what gets done, not what gets planned.',
    relatedMission: 'Complete a Creative Mission',
    relatedProduct: 'Build Different Tee',
    relatedRank: 'Lieutenant',
  },
  {
    id: 8,
    slug: 'every-drop-has-meaning',
    title: 'Article VIII — Every Drop Has Meaning',
    shortTitle: 'Every Drop Has Meaning',
    teaser: 'We do not drop product for the sake of product. Everything means something.',
    rule: 'If it does not mean something, it does not drop.',
    meaning:
      'Every product released by the Cold Empire is connected to the story, the code, the community, or a moment in the empire\'s history. There are no filler drops. There is no mass production without intention.',
    looksLike:
      'Products with lore attached. Limited runs that reference something real. Collections that tell a chapter. Products that mean something to the people who wear them.',
    breaksIt:
      'Dropping product for cash without context. Releasing things that contradict the identity. Saturating the market with meaningless inventory.',
    whyItMatters:
      'When a product means something, it holds value. When it is just a shirt, it is just a shirt. We are not in the shirt business. We are in the signal business.',
    relatedMission: 'Buy a Drop',
    relatedProduct: 'Article VIII Tee',
    relatedRank: 'Associate',
  },
  {
    id: 9,
    slug: 'protect-the-small-crew',
    title: 'Article IX — Protect the Small Crew',
    shortTitle: 'Protect the Small Crew',
    teaser: 'The empire started with a small crew. Never forget where it began.',
    rule: 'The small crew gets protected first.',
    meaning:
      'The people who were there at the beginning — when there was no buzz, no audience, no reason to show up except belief — those people are the foundation. They get protected. They get remembered. They get taken care of.',
    looksLike:
      'Day-one loyalty getting rewarded. Early members getting access first. The inner circle being treated as family, not resource. Remembering who showed up when it was nothing.',
    breaksIt:
      'Forgetting the crew when the platform grows. Replacing loyal people with bigger names. Using early members\' work without crediting them.',
    whyItMatters:
      'If you build it with people and then leave them behind, you did not build an empire. You built a hustle. Empires last because the foundation is human.',
    relatedMission: 'Invite a Day-One',
    relatedProduct: 'Day One Hoodie',
    relatedRank: 'Capo',
  },
  {
    id: 10,
    slug: 'the-brand-is-the-territory',
    title: 'Article X — The Brand Is the Territory',
    shortTitle: 'The Brand Is the Territory',
    teaser: 'Everywhere the signal appears, it claims territory. Protect what it claims.',
    rule: 'The brand is not a logo. It is a territory. Defend it.',
    meaning:
      'When the Cold Empire brand appears somewhere — a sticker on a wall, a hoodie in a photo, a post online — that is territory. It represents the empire\'s presence, standards, and signal in that space.',
    looksLike:
      'Keeping brand quality consistent. Not allowing the name to be used by people who do not represent it. Making sure the brand\'s appearance always reflects the code.',
    breaksIt:
      'Letting low-quality representation slide because it is convenient. Letting people use the name without accountability. Ignoring how the brand is perceived in new spaces.',
    whyItMatters:
      'Territory is won slowly and lost fast. One bad look in the wrong space can set the signal back. Protecting the brand is protecting the future of every member.',
    relatedMission: 'Report a Brand Misuse',
    relatedProduct: 'Cold Empire Flag',
    relatedRank: 'Don',
  },
  {
    id: 11,
    slug: 'move-quiet-hit-loud',
    title: 'Article XI — Move Quiet, Hit Loud',
    shortTitle: 'Move Quiet, Hit Loud',
    teaser: 'Announce nothing. Deliver everything. Let the arrival speak.',
    rule: 'Build in silence. Launch with impact.',
    meaning:
      'The empire does not announce its moves before they are ready. It does not tease what it cannot deliver. It builds in silence and arrives with force. The reveal is the announcement.',
    looksLike:
      'Keeping projects internal until they are ready. Dropping things without warning when the moment is right. Letting the product do the talking instead of the promo.',
    breaksIt:
      'Announcing too early. Hyping things that do not land. Over-explaining what you are doing before you do it. Letting strategy leak before execution.',
    whyItMatters:
      'Surprise is a weapon. Anticipation is a tool. When you move quiet, you control both. When you talk too much, you give both away.',
    relatedMission: 'Complete a Silent Mission',
    relatedProduct: 'Move Quiet Tee',
    relatedRank: 'Don',
  },
  {
    id: 12,
    slug: 'the-game-never-ends',
    title: 'Article XII — The Game Never Ends',
    shortTitle: 'The Game Never Ends',
    teaser: 'There is no finish line. There is only the next level.',
    rule: 'When you think you are done, you are just between moves.',
    meaning:
      'The Cold Empire is not a project with an end date. It is a living system. The missions do not stop. The drops do not stop. The game does not stop. The moment you think you have arrived is the moment you start falling behind.',
    looksLike:
      'Always looking for the next mission. Staying engaged between events. Treating rank not as an end but as a starting point. Continuing to contribute after you have received.',
    breaksIt:
      'Going quiet after reaching a rank. Only showing up when there is something new to take. Treating the empire like a store instead of a game.',
    whyItMatters:
      'The game rewards people who play it continuously. Consistency compounds. The members who keep showing up end up with everything. The ones who stop always lose ground.',
    relatedMission: 'Complete 10 Missions',
    relatedProduct: 'The Game Never Ends Hoodie',
    relatedRank: 'Boss',
  },
  {
    id: 13,
    slug: 'stay-cold',
    title: 'Article XIII — Stay Cold',
    shortTitle: 'Stay Cold',
    teaser: 'Cold is not a temperature. It is a state of mind. Stay in it.',
    rule: 'When things get hot, stay cold.',
    meaning:
      'Cold means calculated. Controlled. Clear. When things go wrong — when a drop fails, when drama hits, when pressure comes — the response of a Cold Empire member is never reactive. It is cold. Steady. Strategic.',
    looksLike:
      'Not responding to bait. Not making emotional decisions in public. Letting others react while you plan. Keeping the energy clean even when the room gets messy.',
    breaksIt:
      'Public drama. Reactive posts. Burning bridges out of emotion. Letting outside noise change your inside direction. Getting hot when you should get cold.',
    whyItMatters:
      'Hot burns out. Cold lasts. Every empire that collapsed did so because someone got hot at the wrong moment. The ones that survive are the ones who stayed cold when it mattered most.',
    relatedMission: 'Hold the Line Mission',
    relatedProduct: 'Stay Cold Hoodie',
    relatedRank: 'Boss',
  },
]

export function getArticleBySlug(slug: string): ColdCodeArticle | undefined {
  return coldCodeArticles.find((a) => a.slug === slug)
}

export function getAdjacentArticles(id: number) {
  const prev = coldCodeArticles.find((a) => a.id === id - 1) ?? null
  const next = coldCodeArticles.find((a) => a.id === id + 1) ?? null
  return { prev, next }
}
