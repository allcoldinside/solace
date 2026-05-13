import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="border-t border-cold-gray/40 bg-cold-dark mt-20">
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
          <div>
            <p className="text-xs tracking-widest uppercase text-cold-smoke mb-4">Empire</p>
            <div className="flex flex-col gap-2">
              <Link href="/door" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">The Door</Link>
              <Link href="/hq" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">HQ</Link>
              <Link href="/ccc" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">Cold&apos;s Cannabis Club</Link>
              <Link href="/ib6" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">Ice Bong Six</Link>
              <Link href="/cartel" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">Cold Cartel</Link>
            </div>
          </div>
          <div>
            <p className="text-xs tracking-widest uppercase text-cold-smoke mb-4">Content</p>
            <div className="flex flex-col gap-2">
              <Link href="/cold-code" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">Cold Code</Link>
              <Link href="/broadcasts" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">Broadcasts</Link>
              <Link href="/events" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">Events</Link>
            </div>
          </div>
          <div>
            <p className="text-xs tracking-widest uppercase text-cold-smoke mb-4">Store</p>
            <div className="flex flex-col gap-2">
              <Link href="/store" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">Shop</Link>
              <Link href="/store?collection=Wear+the+Signal" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">Wear the Signal</Link>
              <Link href="/store?collection=Find+the+Door" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">Find the Door</Link>
              <Link href="/store?tag=ib6" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">IB6 Gear</Link>
            </div>
          </div>
          <div>
            <p className="text-xs tracking-widest uppercase text-cold-smoke mb-4">Account</p>
            <div className="flex flex-col gap-2">
              <Link href="/auth/login" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">Login</Link>
              <Link href="/auth/register" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">Register</Link>
              <Link href="/portal" className="text-cold-gray-light hover:text-cold-green text-sm font-mono transition-colors">Member Portal</Link>
            </div>
          </div>
        </div>

        <div className="border-t border-cold-gray/40 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-cold-smoke font-mono text-xs tracking-widest">
            COLD EMPIRE © {new Date().getFullYear()} — GETHIGH.LIFE
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            {['About', 'Contact', 'FAQ', 'Shipping', 'Returns', 'Privacy', 'Terms', 'Age Policy'].map((item) => (
              <span key={item} className="text-cold-gray-light font-mono text-xs tracking-wide cursor-default hover:text-cold-smoke transition-colors">
                {item}
              </span>
            ))}
          </div>
          <p className="text-cold-gray font-mono text-xs">
            21+ only where required by law.
          </p>
        </div>
      </div>
    </footer>
  )
}
