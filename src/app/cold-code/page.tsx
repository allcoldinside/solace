import { coldCodeArticles } from '@/data/coldCode'
import Link from 'next/link'
import EmailCapture from '@/components/ui/EmailCapture'

export default function ColdCodePage() {
  return (
    <div className="min-h-screen bg-cold-black px-6 lg:px-16 max-w-6xl mx-auto py-16">
      {/* Header */}
      <div className="mb-16">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">THE LAW</p>
        <h1 className="text-5xl lg:text-6xl font-mono text-cold-white mb-6">Cold Code</h1>
        <p className="text-cold-smoke font-mono text-xl max-w-xl leading-relaxed">
          Rules before rank. Loyalty before noise.
        </p>
      </div>

      {/* Articles */}
      <div className="space-y-3 mb-20">
        {coldCodeArticles.map((article, i) => (
          <Link
            key={article.slug}
            href={`/cold-code/${article.slug}`}
            className="group flex items-start gap-6 border border-cold-gray/40 hover:border-cold-green/50 bg-cold-charcoal hover:bg-cold-green/3 p-5 transition-all duration-200"
          >
            <span className="text-cold-smoke font-mono text-xs w-6 mt-0.5 flex-shrink-0">{String(i + 1).padStart(2, '0')}</span>
            <div className="flex-1">
              <h2 className="text-cold-white group-hover:text-cold-green font-mono text-sm tracking-wide mb-1 transition-colors">
                {article.shortTitle}
              </h2>
              <p className="text-cold-smoke font-mono text-xs leading-relaxed">{article.teaser}</p>
            </div>
            <span className="text-cold-green/30 group-hover:text-cold-green font-mono text-sm transition-colors flex-shrink-0 mt-0.5">→</span>
          </Link>
        ))}
      </div>

      {/* Email */}
      <div className="border-t border-cold-gray/40 pt-12 max-w-lg">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">NEXT SIGNAL</p>
        <h2 className="text-xl font-mono text-cold-white mb-2">Want the next signal?</h2>
        <p className="text-cold-smoke font-mono text-sm mb-6">Lore leaks, drop alerts, and early access.</p>
        <EmailCapture source="cold-code" tags="lore,drops" />
      </div>
    </div>
  )
}
