'use client'

import { useState } from 'react'
import { ranks } from '@/data/ranks'
import Link from 'next/link'

export default function CartelPage() {
  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(false)
  const [form, setForm] = useState({ email: '', alias: '', interest: '', discord: '' })
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await fetch('/api/cartel/request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (res.ok) {
        setSubmitted(true)
      } else {
        const data = await res.json()
        setError(data.error ?? 'Something went wrong.')
      }
    } catch {
      setError('Connection failed. Try again.')
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-cold-black">
      {/* Hero */}
      <section className="min-h-[70vh] flex flex-col items-start justify-center px-6 lg:px-16 max-w-6xl mx-auto relative">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_30%_50%,rgba(0,255,65,0.02)_0%,transparent_60%)]" />
        <div className="relative z-10">
          <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">COLD CARTEL</p>
          <h1 className="text-5xl lg:text-7xl font-mono text-cold-white leading-tight mb-6">
            The private<br />layer.
          </h1>
          <p className="text-cold-smoke font-mono text-xl max-w-lg mb-3 leading-relaxed">
            Not everyone gets in.
          </p>
          <p className="text-cold-smoke font-mono text-xl max-w-lg mb-10">
            Not everyone needs to.
          </p>
          <div className="flex flex-wrap gap-4">
            <a href="#request" className="bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase px-8 py-4 hover:opacity-90 transition-opacity">
              Request Access
            </a>
            <Link href="/cold-code" className="border border-cold-green text-cold-green font-mono tracking-widest uppercase px-8 py-4 hover:bg-cold-green hover:text-cold-black transition-all">
              Read the Code
            </Link>
          </div>
        </div>
      </section>

      {/* What it is */}
      <section className="px-6 lg:px-16 max-w-6xl mx-auto py-16 border-t border-cold-gray/40">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">WHAT IT IS</p>
        <div className="max-w-2xl">
          <p className="text-cold-white font-mono text-lg leading-relaxed mb-4">
            Cold Cartel is the membership layer of the Cold Empire.
          </p>
          <p className="text-cold-smoke font-mono text-sm leading-relaxed">
            It connects lore, rank, rewards, events, hidden content, and future gated access. It is not a subscription. It is not a club you join because you paid. It is something you earn through showing up, reading the code, completing missions, and building something inside the empire.
          </p>
        </div>
      </section>

      {/* Rank Structure */}
      <section className="px-6 lg:px-16 max-w-6xl mx-auto py-16 border-t border-cold-gray/40">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">RANK STRUCTURE</p>
        <h2 className="text-2xl font-mono text-cold-white mb-8">Six levels. Every one earned.</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {ranks.map((rank) => (
            <div key={rank.id} className="border border-cold-gray/40 bg-cold-charcoal p-5 relative overflow-hidden">
              <div
                className="absolute top-0 left-0 w-full h-0.5"
                style={{ background: rank.color, opacity: 0.6 }}
              />
              <div className="flex items-center gap-3 mb-3">
                <span className="font-mono text-xs text-cold-smoke">#{rank.level}</span>
                <h3 className="font-mono text-sm" style={{ color: rank.color }}>
                  {rank.name}
                </h3>
              </div>
              <p className="text-cold-smoke font-mono text-xs leading-relaxed mb-3">{rank.description}</p>
              <div className="space-y-1">
                {rank.perks.slice(0, 3).map((perk) => (
                  <p key={perk} className="text-cold-white font-mono text-xs flex items-start gap-2">
                    <span style={{ color: rank.color }}>→</span> {perk}
                  </p>
                ))}
                {rank.perks.length > 3 && (
                  <p className="text-cold-smoke font-mono text-xs">+{rank.perks.length - 3} more</p>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Cold Code CTA */}
      <section className="px-6 lg:px-16 max-w-6xl mx-auto py-12 border-t border-cold-gray/40">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
          <div>
            <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-2">BEFORE RANK COMES CODE</p>
            <p className="text-cold-white font-mono text-lg">Read the 13 articles. Then come back.</p>
          </div>
          <Link href="/cold-code" className="bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase px-8 py-3 hover:opacity-90 transition-opacity whitespace-nowrap">
            Read the Cold Code
          </Link>
        </div>
      </section>

      {/* Request Access */}
      <section id="request" className="px-6 lg:px-16 max-w-6xl mx-auto py-16 border-t border-cold-gray/40">
        <div className="max-w-lg">
          <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">REQUEST ACCESS</p>
          <h2 className="text-2xl font-mono text-cold-white mb-2">Everybody wants the room.</h2>
          <p className="text-cold-smoke font-mono text-sm mb-8">
            Not everybody understands the code. Curiosity gets people noticed. Sometimes.
          </p>

          {submitted ? (
            <div className="border border-cold-green/40 bg-cold-green/5 p-6">
              <p className="text-cold-green font-mono text-sm mb-2">✓ Request received.</p>
              <p className="text-cold-white font-mono text-sm">Watch for the next signal.</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-cold-smoke font-mono text-xs tracking-wide mb-2">EMAIL *</label>
                <input
                  type="email"
                  required
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  className="w-full bg-cold-charcoal border border-cold-gray text-cold-white font-mono px-4 py-3 text-sm focus:outline-none focus:border-cold-green transition-colors"
                  placeholder="your@email.com"
                />
              </div>
              <div>
                <label className="block text-cold-smoke font-mono text-xs tracking-wide mb-2">ALIAS / NAME</label>
                <input
                  type="text"
                  value={form.alias}
                  onChange={(e) => setForm({ ...form, alias: e.target.value })}
                  className="w-full bg-cold-charcoal border border-cold-gray text-cold-white font-mono px-4 py-3 text-sm focus:outline-none focus:border-cold-green transition-colors"
                  placeholder="What do people call you?"
                />
              </div>
              <div>
                <label className="block text-cold-smoke font-mono text-xs tracking-wide mb-2">DISCORD NAME</label>
                <input
                  type="text"
                  value={form.discord}
                  onChange={(e) => setForm({ ...form, discord: e.target.value })}
                  className="w-full bg-cold-charcoal border border-cold-gray text-cold-white font-mono px-4 py-3 text-sm focus:outline-none focus:border-cold-green transition-colors"
                  placeholder="username#0000"
                />
              </div>
              <div>
                <label className="block text-cold-smoke font-mono text-xs tracking-wide mb-2">INTEREST</label>
                <select
                  value={form.interest}
                  onChange={(e) => setForm({ ...form, interest: e.target.value })}
                  className="w-full bg-cold-charcoal border border-cold-gray text-cold-white font-mono px-4 py-3 text-sm focus:outline-none focus:border-cold-green transition-colors"
                >
                  <option value="">Select one</option>
                  <option value="gaming">Gaming / IB6</option>
                  <option value="merch">Merch / Drops</option>
                  <option value="events">Events</option>
                  <option value="lore">Lore / ARG</option>
                  <option value="creator">Creator / Collab</option>
                  <option value="business">Business</option>
                </select>
              </div>
              {error && <p className="text-red-400 font-mono text-xs">{error}</p>}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase py-4 hover:opacity-90 transition-opacity disabled:opacity-50"
              >
                {loading ? '...' : 'Request Access'}
              </button>
            </form>
          )}
        </div>
      </section>
    </div>
  )
}
