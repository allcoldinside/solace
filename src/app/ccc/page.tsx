import { getFeaturedProducts, formatPrice } from '@/data/products'
import Link from 'next/link'
import EmailCapture from '@/components/ui/EmailCapture'

export default function CCCPage() {
  const featured = getFeaturedProducts().slice(0, 4)

  return (
    <div className="min-h-screen bg-cold-black">
      {/* Hero */}
      <section className="min-h-[70vh] flex flex-col items-start justify-center px-6 lg:px-16 max-w-6xl mx-auto">
        <p className="text-xs tracking-widest uppercase text-cold-green font-mono mb-4">COLD&apos;S CANNABIS CLUB</p>
        <h1 className="text-5xl lg:text-7xl font-mono text-cold-white leading-tight mb-6">
          CCC
        </h1>
        <p className="text-cold-smoke font-mono text-xl max-w-xl mb-10 leading-relaxed">
          A lifestyle brand for the ones who live outside the default settings.
        </p>
        <div className="flex flex-wrap gap-4">
          <Link href="/store" className="bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase px-8 py-4 hover:opacity-90 transition-opacity">
            Enter the Store
          </Link>
          <Link href="/cold-code" className="border border-cold-green text-cold-green font-mono tracking-widest uppercase px-8 py-4 hover:bg-cold-green hover:text-cold-black transition-all">
            Learn the Story
          </Link>
        </div>
      </section>

      {/* What CCC Is */}
      <section className="px-6 lg:px-16 max-w-6xl mx-auto py-20 border-t border-cold-gray/40">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">WHAT IT IS</p>
        <div className="grid lg:grid-cols-2 gap-12 items-start">
          <div>
            <h2 className="text-3xl font-mono text-cold-white mb-6">The public face of the empire.</h2>
            <div className="space-y-4 text-cold-smoke font-mono text-sm leading-relaxed">
              <p>
                Cold&apos;s Cannabis Club is the lifestyle brand. It carries the aesthetic, the apparel, the attitude, the drops, and the real-world identity of the Cold Empire.
              </p>
              <p>
                CCC is where the public meets the empire. You do not need to know the full story to wear the signal. But once you start asking questions, the story finds you.
              </p>
              <p>
                Black-on-black. Neon accents. Hidden symbols. Every piece is designed to be recognized by the people who deserve to recognize it.
              </p>
            </div>
          </div>
          <div className="border border-cold-gray/40 p-8 bg-cold-charcoal">
            <h3 className="text-cold-green font-mono text-lg mb-4">What CCC carries</h3>
            <ul className="space-y-2 text-cold-smoke font-mono text-sm">
              {['Hoodies and heavy pulls', 'Cold Code tees', 'Limited graphic drops', 'Stickers and signals', 'Hats and accessories', 'Seasonal releases', 'Cartel-tier exclusives'].map((item) => (
                <li key={item} className="flex items-center gap-3">
                  <span className="text-cold-green">→</span> {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* Featured Drops */}
      <section className="px-6 lg:px-16 max-w-6xl mx-auto py-16 border-t border-cold-gray/40">
        <div className="flex items-end justify-between mb-8">
          <div>
            <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-2">FEATURED DROPS</p>
            <h2 className="text-2xl font-mono text-cold-white">Current Signal</h2>
          </div>
          <Link href="/store" className="text-cold-green font-mono text-xs tracking-widest uppercase hover:opacity-70 transition-opacity">
            View All →
          </Link>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {featured.map((product) => (
            <Link key={product.id} href={`/store/${product.slug}`} className="group block bg-cold-charcoal border border-cold-gray hover:border-cold-green/50 p-4 transition-all">
              <div className="aspect-square bg-cold-dark mb-4 flex items-center justify-center">
                <span className="text-cold-smoke font-mono text-xs tracking-wide">[ IMAGE ]</span>
              </div>
              <h3 className="text-cold-white group-hover:text-cold-green font-mono text-sm mb-1 transition-colors">{product.name}</h3>
              <p className="text-cold-smoke font-mono text-xs mb-2">{product.collection}</p>
              <p className="text-cold-green font-mono text-sm">{formatPrice(product.price)}</p>
            </Link>
          ))}
        </div>
      </section>

      {/* The Signal */}
      <section className="px-6 lg:px-16 max-w-6xl mx-auto py-20 border-t border-cold-gray/40">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">THE SIGNAL</p>
        <h2 className="text-3xl font-mono text-cold-white mb-8">Visual identity explained.</h2>
        <div className="grid lg:grid-cols-3 gap-6 mb-10">
          {[
            { title: 'Black on Black', desc: 'The signal is there. You either see it or you do not.' },
            { title: 'Neon Accents', desc: 'Green. The one color that cuts through the dark.' },
            { title: 'Hidden Symbols', desc: 'Cold Code references embedded in every design.' },
          ].map((item) => (
            <div key={item.title} className="border border-cold-gray/40 p-6 bg-cold-charcoal">
              <h3 className="text-cold-green font-mono text-sm tracking-wide mb-2">{item.title}</h3>
              <p className="text-cold-smoke font-mono text-xs leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
        <blockquote className="border-l-2 border-cold-green pl-6 py-2">
          <p className="text-cold-white font-mono text-xl">&ldquo;Some people wear logos. Some people wear signals.&rdquo;</p>
        </blockquote>
        <div className="mt-6">
          <Link href="/store" className="bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase px-8 py-3 hover:opacity-90 transition-opacity inline-block">
            Wear the Signal
          </Link>
        </div>
      </section>

      {/* Email capture */}
      <section className="px-6 lg:px-16 max-w-6xl mx-auto py-16 border-t border-cold-gray/40">
        <div className="max-w-lg">
          <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">JOIN THE LIST</p>
          <h2 className="text-2xl font-mono text-cold-white mb-2">Get drop alerts, lore leaks, and early access.</h2>
          <p className="text-cold-smoke font-mono text-sm mb-6">No noise. Only signal.</p>
          <EmailCapture source="ccc" tags="ccc,drops" ctaText="Get the Signal" />
        </div>
      </section>
    </div>
  )
}
