import Link from 'next/link'

export default function CheckoutSuccessPage() {
  return (
    <div className="min-h-screen bg-cold-black flex flex-col items-center justify-center px-6 text-center">
      <div className="max-w-lg">
        <div className="w-16 h-16 border border-cold-green bg-cold-green/10 flex items-center justify-center mx-auto mb-8">
          <span className="text-cold-green text-2xl">✓</span>
        </div>

        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">ORDER CONFIRMED</p>
        <h1 className="text-4xl font-mono text-cold-white mb-4">Package secured.</h1>
        <p className="text-cold-smoke font-mono text-lg mb-10">
          Watch your inbox. The signal continues there.
        </p>

        <div className="grid sm:grid-cols-3 gap-3 mb-10">
          <a
            href={process.env.NEXT_PUBLIC_DISCORD_INVITE_URL ?? '#'}
            target="_blank"
            rel="noopener noreferrer"
            className="border border-cold-gray bg-cold-charcoal p-4 text-left hover:border-cold-green/50 transition-all group"
          >
            <p className="text-cold-green font-mono text-xs tracking-widest uppercase mb-2 group-hover:opacity-80">Discord</p>
            <p className="text-cold-smoke font-mono text-xs">Join the community. The lobby is open.</p>
          </a>

          <Link href="/cold-code" className="border border-cold-gray bg-cold-charcoal p-4 text-left hover:border-cold-green/50 transition-all group">
            <p className="text-cold-green font-mono text-xs tracking-widest uppercase mb-2 group-hover:opacity-80">Cold Code</p>
            <p className="text-cold-smoke font-mono text-xs">Read Article I. Understand what you are wearing.</p>
          </Link>

          <Link href="/cartel" className="border border-cold-gray bg-cold-charcoal p-4 text-left hover:border-cold-green/50 transition-all group">
            <p className="text-cold-green font-mono text-xs tracking-widest uppercase mb-2 group-hover:opacity-80">Cold Cartel</p>
            <p className="text-cold-smoke font-mono text-xs">Request access to the private layer.</p>
          </Link>
        </div>

        <Link href="/store" className="text-cold-smoke hover:text-cold-green font-mono text-xs tracking-widest uppercase transition-colors">
          ← Continue Shopping
        </Link>
      </div>
    </div>
  )
}
