import { getEventsByTag } from '@/data/events'
import { getProductsByTag, formatPrice } from '@/data/products'
import Link from 'next/link'
import EmailCapture from '@/components/ui/EmailCapture'

export default function IB6Page() {
  const events = getEventsByTag('ib6')
  const merch = getProductsByTag('ib6')

  return (
    <div className="min-h-screen bg-cold-black">
      {/* Hero */}
      <section className="min-h-[70vh] flex flex-col items-start justify-center px-6 lg:px-16 max-w-6xl mx-auto">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">ICE BONG SIX</p>
        <h1 className="text-5xl lg:text-7xl font-mono text-cold-white leading-tight mb-6">
          IB6
        </h1>
        <p className="text-cold-smoke font-mono text-xl max-w-xl mb-3 leading-relaxed">
          Stoner gamer community. No fake league energy.
        </p>
        <p className="text-cold-green font-mono text-lg mb-10">
          Just the lobby, the crew, and the chaos.
        </p>
        <div className="flex flex-wrap gap-4">
          <a
            href={process.env.NEXT_PUBLIC_DISCORD_INVITE_URL ?? '#'}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase px-8 py-4 hover:opacity-90 transition-opacity"
          >
            Join Discord
          </a>
          <Link href="/events" className="border border-cold-green text-cold-green font-mono tracking-widest uppercase px-8 py-4 hover:bg-cold-green hover:text-cold-black transition-all">
            See Events
          </Link>
        </div>
      </section>

      {/* What IB6 Is */}
      <section className="px-6 lg:px-16 max-w-6xl mx-auto py-20 border-t border-cold-gray/40">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">THE LOBBY</p>
        <div className="grid lg:grid-cols-2 gap-12">
          <div>
            <h2 className="text-3xl font-mono text-cold-white mb-6">The gaming wing of the Cold Empire.</h2>
            <div className="space-y-4 text-cold-smoke font-mono text-sm leading-relaxed">
              <p>
                IB6 is where the community gathers, plays, streams, talks trash, joins events, and builds the culture.
              </p>
              <p>
                We do not care about your KD ratio. We do not have a sponsorship deal that requires us to pretend to care about competitive integrity. We just want to play and have a good time.
              </p>
              <p>
                For the fkn fun of it. That is the entire mission statement.
              </p>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            {[
              { label: 'Game Nights', desc: 'Weekly lobby sessions. Multiple games.' },
              { label: 'Tournaments', desc: 'Real prizes. Real chaos.' },
              { label: 'Stream Nights', desc: 'Watch parties and live events.' },
              { label: 'Challenges', desc: 'Stoner gamer specific. You will understand.' },
            ].map((item) => (
              <div key={item.label} className="border border-cold-gray/40 p-4 bg-cold-charcoal">
                <h3 className="text-cold-green font-mono text-sm mb-1">{item.label}</h3>
                <p className="text-cold-smoke font-mono text-xs leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Enter the Lobby */}
      <section className="px-6 lg:px-16 max-w-6xl mx-auto py-16 border-t border-cold-gray/40">
        <div className="bg-cold-charcoal border border-cold-green/30 p-8 lg:p-12 text-center">
          <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">JOIN THE LOBBY</p>
          <h2 className="text-3xl font-mono text-cold-white mb-4">The lobby opens when you step in.</h2>
          <p className="text-cold-smoke font-mono text-sm mb-8 max-w-md mx-auto">
            Discord is the home base. Events get announced there. Missions get completed there. The crew lives there.
          </p>
          <a
            href={process.env.NEXT_PUBLIC_DISCORD_INVITE_URL ?? '#'}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase px-10 py-4 hover:opacity-90 transition-opacity inline-block"
          >
            Enter Discord
          </a>
        </div>
      </section>

      {/* Events */}
      {events.length > 0 && (
        <section className="px-6 lg:px-16 max-w-6xl mx-auto py-16 border-t border-cold-gray/40">
          <div className="flex items-end justify-between mb-8">
            <div>
              <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-2">UPCOMING</p>
              <h2 className="text-2xl font-mono text-cold-white">Events</h2>
            </div>
            <Link href="/events" className="text-cold-green font-mono text-xs tracking-widest uppercase hover:opacity-70">
              All Events →
            </Link>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {events.map((event) => (
              <div key={event.id} className="border border-cold-gray/40 bg-cold-charcoal p-5">
                <div className="flex items-center gap-2 mb-3">
                  <span className={`text-xs font-mono tracking-widest uppercase px-2 py-0.5 ${event.type === 'online' ? 'bg-cold-green/10 text-cold-green border border-cold-green/30' : 'bg-cold-gold/10 text-cold-gold border border-cold-gold/30'}`}>
                    {event.type}
                  </span>
                </div>
                <h3 className="text-cold-white font-mono text-sm mb-1">{event.title}</h3>
                <p className="text-cold-smoke font-mono text-xs mb-3 leading-relaxed">{event.description}</p>
                <div className="text-cold-smoke font-mono text-xs space-y-1">
                  <p>📅 {event.date} — {event.time}</p>
                  <p>📍 {event.location}</p>
                  {event.prize && <p>🏆 {event.prize}</p>}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Gamer tag submit */}
      <section className="px-6 lg:px-16 max-w-6xl mx-auto py-16 border-t border-cold-gray/40">
        <div className="max-w-lg">
          <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">SUBMIT YOUR TAG</p>
          <h2 className="text-2xl font-mono text-cold-white mb-2">Let the lobby know you exist.</h2>
          <p className="text-cold-smoke font-mono text-sm mb-6">Drop your email and gamer tag. We will find you.</p>
          <EmailCapture
            source="ib6"
            tags="ib6,gaming"
            placeholder="your@email.com"
            ctaText="Submit"
            successMessage="Tag logged. Watch for the invite."
          />
        </div>
      </section>

      {/* IB6 Merch */}
      {merch.length > 0 && (
        <section className="px-6 lg:px-16 max-w-6xl mx-auto py-16 border-t border-cold-gray/40">
          <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">IB6 GEAR</p>
          <h2 className="text-2xl font-mono text-cold-white mb-6">Wear IB6</h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {merch.map((product) => (
              <Link key={product.id} href={`/store/${product.slug}`} className="group block bg-cold-charcoal border border-cold-gray hover:border-cold-green/50 p-4 transition-all">
                <div className="aspect-square bg-cold-dark mb-4 flex items-center justify-center">
                  <span className="text-cold-smoke font-mono text-xs">[ IMAGE ]</span>
                </div>
                <h3 className="text-cold-white group-hover:text-cold-green font-mono text-sm mb-1 transition-colors">{product.name}</h3>
                <p className="text-cold-green font-mono text-sm">{formatPrice(product.price)}</p>
              </Link>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
