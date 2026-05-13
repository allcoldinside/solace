'use client'

import { useState } from 'react'
import { getUpcomingEvents } from '@/data/events'

export default function EventsPage() {
  const events = getUpcomingEvents()
  const [submitted, setSubmitted] = useState(false)
  const [form, setForm] = useState({ name: '', email: '', idea: '' })
  const [loading, setLoading] = useState(false)

  async function handleCollab(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    await new Promise((r) => setTimeout(r, 800))
    setSubmitted(true)
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-cold-black px-6 lg:px-16 max-w-6xl mx-auto py-16">
      {/* Header */}
      <div className="mb-12">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">COLD EMPIRE</p>
        <h1 className="text-4xl lg:text-5xl font-mono text-cold-white mb-4">Events</h1>
        <p className="text-cold-smoke font-mono text-xl">The signal leaves the screen.</p>
      </div>

      {/* Events */}
      <section className="mb-20">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-6">UPCOMING</p>
        {events.length === 0 ? (
          <div className="border border-cold-gray/40 bg-cold-charcoal p-8 text-center">
            <p className="text-cold-smoke font-mono text-sm">Watch Discord for the next drop. They happen without warning.</p>
          </div>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-2 gap-4">
            {events.map((event) => (
              <div key={event.id} className="border border-cold-gray/40 bg-cold-charcoal p-6">
                <div className="flex items-center gap-3 mb-4">
                  <span className={`text-xs font-mono tracking-widest uppercase px-2 py-0.5 border ${
                    event.type === 'irl'
                      ? 'border-cold-gold/40 text-cold-gold'
                      : event.type === 'stream'
                      ? 'border-cold-green/40 text-cold-green'
                      : 'border-cold-smoke/40 text-cold-smoke'
                  }`}>
                    {event.type === 'irl' ? '📍 IRL' : event.type === 'stream' ? '📡 Stream' : '🎮 Online'}
                  </span>
                  {event.tags.includes('featured') && (
                    <span className="text-xs font-mono text-cold-green border border-cold-green/30 px-2 py-0.5">Featured</span>
                  )}
                </div>

                <h2 className="text-cold-white font-mono text-lg mb-2">{event.title}</h2>
                <p className="text-cold-smoke font-mono text-xs mb-4 leading-relaxed">{event.description}</p>

                <div className="space-y-1 mb-4 text-cold-smoke font-mono text-xs">
                  <p>📅 {new Date(event.date).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })}</p>
                  <p>⏰ {event.time}</p>
                  <p>📍 {event.location}</p>
                  {event.rules && <p>📋 {event.rules}</p>}
                  {event.prize && <p>🏆 {event.prize}</p>}
                </div>

                {event.discordEventUrl ? (
                  <a
                    href={event.discordEventUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-block border border-cold-green text-cold-green font-mono text-xs tracking-widest uppercase px-4 py-2 hover:bg-cold-green hover:text-cold-black transition-all"
                  >
                    Join Discord
                  </a>
                ) : (
                  <button className="border border-cold-gray text-cold-smoke font-mono text-xs tracking-widest uppercase px-4 py-2 hover:border-cold-green hover:text-cold-white transition-all">
                    RSVP — Details in Discord
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Partner section */}
      <section className="border-t border-cold-gray/40 pt-16">
        <div className="grid lg:grid-cols-2 gap-12">
          <div>
            <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">PARTNER WITH US</p>
            <h2 className="text-3xl font-mono text-cold-white mb-4">We bring the vibe.</h2>
            <p className="text-cold-white font-mono text-lg mb-3">
              You bring the food, space, or crowd.
            </p>
            <p className="text-cold-smoke font-mono text-sm leading-relaxed">
              We are open to food truck collabs, venue partnerships, creator crossovers, and local business connections. If it makes sense for the empire, we are interested.
            </p>
            <p className="text-cold-green font-mono text-sm mt-4">Everybody eats.</p>
          </div>

          <div>
            {submitted ? (
              <div className="border border-cold-green/40 bg-cold-green/5 p-6">
                <p className="text-cold-green font-mono text-sm mb-2">✓ Pitch received.</p>
                <p className="text-cold-white font-mono text-sm">We will be in touch if it fits.</p>
              </div>
            ) : (
              <form onSubmit={handleCollab} className="space-y-4">
                <div>
                  <label className="block text-cold-smoke font-mono text-xs tracking-wide mb-2">NAME / BUSINESS</label>
                  <input
                    type="text"
                    required
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    className="w-full bg-cold-charcoal border border-cold-gray text-cold-white font-mono px-4 py-3 text-sm focus:outline-none focus:border-cold-green transition-colors"
                    placeholder="Who are you?"
                  />
                </div>
                <div>
                  <label className="block text-cold-smoke font-mono text-xs tracking-wide mb-2">EMAIL</label>
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
                  <label className="block text-cold-smoke font-mono text-xs tracking-wide mb-2">THE PITCH</label>
                  <textarea
                    required
                    rows={4}
                    value={form.idea}
                    onChange={(e) => setForm({ ...form, idea: e.target.value })}
                    className="w-full bg-cold-charcoal border border-cold-gray text-cold-white font-mono px-4 py-3 text-sm focus:outline-none focus:border-cold-green transition-colors resize-none"
                    placeholder="What do you bring? What do you need? Keep it short."
                  />
                </div>
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase py-4 hover:opacity-90 transition-opacity disabled:opacity-50"
                >
                  {loading ? '...' : 'Pitch a Collab'}
                </button>
              </form>
            )}
          </div>
        </div>
      </section>
    </div>
  )
}
