'use client'

import { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import { getActiveMissions, Mission } from '@/data/missions'
import { useRouter } from 'next/navigation'

export default function MissionsPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [proof, setProof] = useState<Record<string, string>>({})
  const [submitting, setSubmitting] = useState<string | null>(null)
  const [submitted, setSubmitted] = useState<string[]>([])
  const [error, setError] = useState<Record<string, string>>({})

  useEffect(() => {
    if (status === 'unauthenticated') router.push('/auth/login')
  }, [status, router])

  const missions = getActiveMissions()

  async function handleSubmit(mission: Mission) {
    if (!session) return
    setSubmitting(mission.id)
    setError((e) => ({ ...e, [mission.id]: '' }))

    try {
      const res = await fetch('/api/missions/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ missionId: mission.id, proof: proof[mission.id] }),
      })
      if (res.ok) {
        setSubmitted((s) => [...s, mission.id])
      } else {
        const data = await res.json()
        setError((e) => ({ ...e, [mission.id]: data.error ?? 'Error submitting.' }))
      }
    } catch {
      setError((e) => ({ ...e, [mission.id]: 'Connection failed.' }))
    }
    setSubmitting(null)
  }

  if (status === 'loading') return <div className="min-h-screen bg-cold-black flex items-center justify-center"><p className="text-cold-smoke font-mono text-sm">Loading...</p></div>

  return (
    <div className="min-h-screen bg-cold-black px-6 lg:px-16 max-w-6xl mx-auto py-12">
      <div className="mb-8">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-2">MEMBER PORTAL</p>
        <h1 className="text-3xl font-mono text-cold-white mb-2">Missions</h1>
        <p className="text-cold-smoke font-mono text-sm">Complete missions to earn points and climb the ranks.</p>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {missions.map((mission) => {
          const done = submitted.includes(mission.id)
          return (
            <div key={mission.id} className={`border p-5 bg-cold-charcoal ${done ? 'border-cold-green/40' : 'border-cold-gray/40'}`}>
              <div className="flex items-start justify-between gap-4 mb-3">
                <div>
                  <span className={`text-xs font-mono tracking-widest uppercase px-2 py-0.5 border mr-2 ${
                    mission.category === 'hidden' ? 'border-cold-gold/40 text-cold-gold' :
                    mission.category === 'event' ? 'border-cold-green/40 text-cold-green' :
                    'border-cold-gray/40 text-cold-smoke'
                  }`}>
                    {mission.category}
                  </span>
                </div>
                <span className="text-cold-green font-mono text-sm font-bold flex-shrink-0">+{mission.points} pts</span>
              </div>

              <h3 className="text-cold-white font-mono text-base mb-1">{mission.title}</h3>
              <p className="text-cold-smoke font-mono text-xs mb-3 leading-relaxed">{mission.description}</p>

              <div className="border border-cold-gray/40 bg-cold-dark p-3 mb-4 text-xs font-mono">
                <p className="text-cold-smoke mb-1">Proof required:</p>
                <p className="text-cold-white">{mission.proofRequired}</p>
              </div>

              <p className="text-cold-smoke font-mono text-xs mb-4">
                Reward: <span className="text-cold-white">{mission.reward}</span>
              </p>

              {done ? (
                <div className="border border-cold-green/40 bg-cold-green/5 p-3 text-cold-green font-mono text-xs">
                  ✓ Submitted — pending review
                </div>
              ) : mission.proofType !== 'none' ? (
                <div>
                  {mission.proofType === 'link' ? (
                    <input
                      type="url"
                      value={proof[mission.id] ?? ''}
                      onChange={(e) => setProof((p) => ({ ...p, [mission.id]: e.target.value }))}
                      className="w-full bg-cold-dark border border-cold-gray text-cold-white font-mono px-3 py-2 text-xs focus:outline-none focus:border-cold-green mb-2 transition-colors"
                      placeholder="https://..."
                    />
                  ) : mission.proofType === 'image' ? (
                    <input
                      type="text"
                      value={proof[mission.id] ?? ''}
                      onChange={(e) => setProof((p) => ({ ...p, [mission.id]: e.target.value }))}
                      className="w-full bg-cold-dark border border-cold-gray text-cold-white font-mono px-3 py-2 text-xs focus:outline-none focus:border-cold-green mb-2 transition-colors"
                      placeholder="Image URL or description..."
                    />
                  ) : (
                    <textarea
                      rows={2}
                      value={proof[mission.id] ?? ''}
                      onChange={(e) => setProof((p) => ({ ...p, [mission.id]: e.target.value }))}
                      className="w-full bg-cold-dark border border-cold-gray text-cold-white font-mono px-3 py-2 text-xs focus:outline-none focus:border-cold-green mb-2 transition-colors resize-none"
                      placeholder="Submit your proof..."
                    />
                  )}
                  {error[mission.id] && <p className="text-red-400 font-mono text-xs mb-2">{error[mission.id]}</p>}
                  <button
                    onClick={() => handleSubmit(mission)}
                    disabled={submitting === mission.id}
                    className="w-full border border-cold-green text-cold-green font-mono text-xs tracking-widest uppercase py-2 hover:bg-cold-green hover:text-cold-black transition-all disabled:opacity-50"
                  >
                    {submitting === mission.id ? '...' : 'Submit'}
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => handleSubmit(mission)}
                  disabled={submitting === mission.id}
                  className="w-full border border-cold-green text-cold-green font-mono text-xs tracking-widest uppercase py-2 hover:bg-cold-green hover:text-cold-black transition-all disabled:opacity-50"
                >
                  {submitting === mission.id ? '...' : 'Mark Complete'}
                </button>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
