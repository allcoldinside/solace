'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

type BotState = 'closed' | 'open' | 'clue'

interface QuickReply {
  label: string
  answer?: string
  route?: string
  followup?: QuickReply[]
}

const mainReplies: QuickReply[] = [
  {
    label: 'What is CCC?',
    answer:
      "Cold's Cannabis Club is the public lifestyle brand. Apparel, drops, and signals for the ones who live outside the default settings.",
    followup: [
      { label: 'Shop the drop', route: '/store' },
      { label: 'Read the story', route: '/ccc' },
    ],
  },
  {
    label: 'What is IB6?',
    answer:
      'Ice Bong Six is the gaming wing. Stoner gamers. No suits. No fake esports energy. Join the lobby.',
    followup: [
      { label: 'Enter Discord', route: process.env.NEXT_PUBLIC_DISCORD_INVITE_URL ?? '/ib6' },
      { label: 'See events', route: '/events' },
    ],
  },
  {
    label: 'What is Cold Cartel?',
    answer:
      "That's the private layer. Rank, missions, hidden content, rewards, and access. Start with the Cold Code. Then request access.",
    followup: [
      { label: 'Read Cold Code', route: '/cold-code' },
      { label: 'Request access', route: '/cartel' },
    ],
  },
  {
    label: 'Where do I shop?',
    route: '/store',
  },
  {
    label: 'How do I join Discord?',
    answer: 'The lobby opens when you step in.',
    followup: [{ label: 'Enter Discord', route: process.env.NEXT_PUBLIC_DISCORD_INVITE_URL ?? '/ib6' }],
  },
  {
    label: "What's the Cold Code?",
    answer:
      '13 articles. Rules before rank. Loyalty before noise. Read them before you ask for access.',
    followup: [{ label: 'Read the Code', route: '/cold-code' }],
  },
  {
    label: "What's new?",
    route: '/hq',
  },
  {
    label: 'I found a clue.',
    answer:
      'Smart. Keep it to yourself until you have solved it. Then submit it through the mission system.',
    followup: [
      { label: 'Submit a mission', route: '/portal/missions' },
      { label: 'Read Cold Code', route: '/cold-code' },
    ],
  },
]

export default function ColdLogicBot() {
  const [state, setState] = useState<BotState>('closed')
  const [currentAnswer, setCurrentAnswer] = useState<string | null>(null)
  const [followup, setFollowup] = useState<QuickReply[] | null>(null)
  const router = useRouter()

  function handleReply(reply: QuickReply) {
    if (reply.route) {
      if (reply.route.startsWith('http')) {
        window.open(reply.route, '_blank')
      } else {
        router.push(reply.route)
        setState('closed')
      }
      return
    }
    if (reply.answer) {
      setCurrentAnswer(reply.answer)
      setFollowup(reply.followup ?? null)
    }
  }

  function reset() {
    setCurrentAnswer(null)
    setFollowup(null)
  }

  return (
    <>
      {/* Floating button */}
      <button
        onClick={() => setState(state === 'closed' ? 'open' : 'closed')}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-cold-charcoal border border-cold-green/50 hover:border-cold-green text-cold-green flex items-center justify-center transition-all hover:shadow-[0_0_20px_rgba(0,255,65,0.3)]"
        aria-label="Cold Logic"
        title="Cold Logic"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <circle cx="12" cy="8" r="3" />
          <path d="M8 8a4 4 0 0 0-4 4v1h16v-1a4 4 0 0 0-4-4" />
          <path d="M7 17l1-4h8l1 4" />
          <path d="M10 17v3M14 17v3" />
          <rect x="9" y="5" width="2" height="1" fill="currentColor" />
          <rect x="13" y="5" width="2" height="1" fill="currentColor" />
        </svg>
      </button>

      {/* Panel */}
      {state === 'open' && (
        <div className="fixed bottom-24 right-6 z-50 w-80 bg-cold-dark border border-cold-green/30 shadow-[0_0_30px_rgba(0,255,65,0.1)]">
          <div className="flex items-center justify-between px-4 py-3 border-b border-cold-gray/40">
            <div>
              <p className="text-cold-green font-mono text-sm font-bold tracking-widest">COLD LOGIC</p>
              <p className="text-cold-smoke font-mono text-xs">Online</p>
            </div>
            <button onClick={() => setState('closed')} className="text-cold-smoke hover:text-cold-white transition-colors text-lg">×</button>
          </div>

          <div className="p-4">
            {currentAnswer ? (
              <>
                <p className="text-cold-white font-mono text-sm leading-relaxed mb-4">{currentAnswer}</p>
                {followup && (
                  <div className="flex flex-col gap-2 mb-4">
                    {followup.map((f) => (
                      <button
                        key={f.label}
                        onClick={() => handleReply(f)}
                        className="text-left text-cold-green font-mono text-xs tracking-wide border border-cold-green/30 px-3 py-2 hover:bg-cold-green hover:text-cold-black transition-all"
                      >
                        → {f.label}
                      </button>
                    ))}
                  </div>
                )}
                <button onClick={reset} className="text-cold-smoke hover:text-cold-white font-mono text-xs tracking-wide transition-colors">
                  ← Back
                </button>
              </>
            ) : (
              <>
                <p className="text-cold-smoke font-mono text-xs mb-4">&quot;Where we headed?&quot;</p>
                <div className="flex flex-col gap-2">
                  {mainReplies.map((r) => (
                    <button
                      key={r.label}
                      onClick={() => handleReply(r)}
                      className="text-left text-cold-white hover:text-cold-green font-mono text-xs tracking-wide border border-cold-gray/40 px-3 py-2 hover:border-cold-green/50 transition-all"
                    >
                      {r.label}
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </>
  )
}
