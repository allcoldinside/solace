import { episodes, series } from '@/data/broadcasts'
import Link from 'next/link'
import EmailCapture from '@/components/ui/EmailCapture'

export default function BroadcastsPage() {
  return (
    <div className="min-h-screen bg-cold-black px-6 lg:px-16 max-w-6xl mx-auto py-16">
      {/* Header */}
      <div className="mb-12">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">COLD EMPIRE</p>
        <h1 className="text-4xl lg:text-5xl font-mono text-cold-white mb-4">Broadcasts</h1>
        <p className="text-cold-smoke font-mono text-xl leading-relaxed">
          Table talks, field notes, lore drops, and smoke-filled strategy.
        </p>
      </div>

      {/* Series tabs */}
      <div className="flex flex-wrap gap-3 mb-12">
        {series.map((s) => (
          <div key={s.id} className="border border-cold-gray/40 px-4 py-2 bg-cold-charcoal">
            <p className="text-cold-white font-mono text-xs">{s.name}</p>
          </div>
        ))}
      </div>

      {/* Episodes */}
      <div className="grid md:grid-cols-2 gap-6 mb-16">
        {episodes.map((ep) => (
          <div key={ep.id} className="border border-cold-gray/40 bg-cold-charcoal p-6 flex flex-col">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-xs font-mono text-cold-smoke tracking-widest uppercase border border-cold-gray/40 px-2 py-0.5">
                {ep.series}
              </span>
              <span className="text-cold-smoke font-mono text-xs">#{ep.number}</span>
              <span className="text-cold-smoke font-mono text-xs ml-auto">{ep.duration}</span>
            </div>

            <h2 className="text-cold-white font-mono text-lg mb-3 leading-tight">{ep.title}</h2>
            <p className="text-cold-smoke font-mono text-xs leading-relaxed mb-4 flex-1">{ep.description}</p>

            {/* Quotes */}
            <div className="space-y-2 mb-4 border-t border-cold-gray/40 pt-4">
              {ep.keyQuotes.slice(0, 2).map((q) => (
                <p key={q} className="text-cold-green/70 font-mono text-xs italic leading-relaxed">{q}</p>
              ))}
            </div>

            {/* Player placeholder */}
            <div className="bg-cold-dark border border-cold-gray/40 p-3 flex items-center gap-3 mb-4">
              <div className="w-8 h-8 bg-cold-green/20 border border-cold-green/30 flex items-center justify-center flex-shrink-0">
                <span className="text-cold-green text-xs">▶</span>
              </div>
              <div className="flex-1 min-w-0">
                <div className="h-1 bg-cold-gray rounded-full">
                  <div className="h-1 bg-cold-green/50 rounded-full w-0" />
                </div>
              </div>
              <span className="text-cold-smoke font-mono text-xs">{ep.duration}</span>
            </div>

            {/* Links */}
            <div className="flex items-center gap-4">
              {ep.relatedCodeSlug && (
                <Link href={`/cold-code/${ep.relatedCodeSlug}`} className="text-cold-green font-mono text-xs tracking-wide hover:opacity-70 transition-opacity">
                  Related Code →
                </Link>
              )}
              {ep.relatedProductSlug && (
                <Link href={`/store/${ep.relatedProductSlug}`} className="text-cold-smoke font-mono text-xs tracking-wide hover:text-cold-white transition-colors">
                  Related Drop →
                </Link>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Email */}
      <div className="border-t border-cold-gray/40 pt-12 max-w-lg">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">NEW TRANSMISSIONS</p>
        <h2 className="text-xl font-mono text-cold-white mb-2">Never miss a broadcast.</h2>
        <p className="text-cold-smoke font-mono text-sm mb-6">Drop alerts, episode releases, and lore leaks.</p>
        <EmailCapture source="broadcasts" tags="broadcasts,lore" />
      </div>
    </div>
  )
}
