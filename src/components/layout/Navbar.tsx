'use client'

import Link from 'next/link'
import { useState } from 'react'
import { useSession } from 'next-auth/react'

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const { data: session } = useSession()

  const links = [
    { href: '/door', label: 'The Door' },
    { href: '/ccc', label: 'CCC' },
    { href: '/store', label: 'Store' },
    { href: '/ib6', label: 'IB6' },
    { href: '/cartel', label: 'Cartel' },
    { href: '/cold-code', label: 'Code' },
    { href: '/broadcasts', label: 'Broadcasts' },
    { href: '/events', label: 'Events' },
  ]

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-cold-black/90 border-b border-cold-gray/40 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 flex items-center justify-between h-14">
        <Link href="/door" className="font-mono text-cold-green tracking-widest uppercase text-sm font-bold hover:opacity-80 transition-opacity">
          COLD EMPIRE
        </Link>

        {/* Desktop */}
        <div className="hidden lg:flex items-center gap-6">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className="text-cold-smoke hover:text-cold-green font-mono text-xs tracking-widest uppercase transition-colors"
            >
              {l.label}
            </Link>
          ))}
          <Link href="/companion" className="text-cold-green font-mono text-xs tracking-widest uppercase border border-cold-green/40 px-3 py-1 hover:bg-cold-green/10 transition-all">
            ◆ APP
          </Link>
          {session ? (
            <Link href="/portal" className="text-cold-green font-mono text-xs tracking-widest uppercase border border-cold-green/40 px-3 py-1 hover:bg-cold-green hover:text-cold-black transition-all">
              Portal
            </Link>
          ) : (
            <Link href="/auth/login" className="text-cold-smoke hover:text-cold-white font-mono text-xs tracking-widest uppercase transition-colors">
              Login
            </Link>
          )}
        </div>

        {/* Mobile toggle */}
        <button
          onClick={() => setOpen(!open)}
          className="lg:hidden text-cold-smoke hover:text-cold-green transition-colors p-2"
          aria-label="Toggle menu"
        >
          <div className={`w-5 h-0.5 bg-current mb-1 transition-all ${open ? 'rotate-45 translate-y-1.5' : ''}`} />
          <div className={`w-5 h-0.5 bg-current mb-1 transition-all ${open ? 'opacity-0' : ''}`} />
          <div className={`w-5 h-0.5 bg-current transition-all ${open ? '-rotate-45 -translate-y-1.5' : ''}`} />
        </button>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="lg:hidden bg-cold-dark border-t border-cold-gray/40 px-4 py-4">
          <div className="flex flex-col gap-4">
            {links.map((l) => (
              <Link
                key={l.href}
                href={l.href}
                onClick={() => setOpen(false)}
                className="text-cold-smoke hover:text-cold-green font-mono text-sm tracking-widest uppercase transition-colors"
              >
                {l.label}
              </Link>
            ))}
            <Link href="/companion" onClick={() => setOpen(false)} className="text-cold-green font-mono text-sm tracking-widest uppercase">
              ◆ APP
            </Link>
            {session ? (
              <Link href="/portal" onClick={() => setOpen(false)} className="text-cold-green font-mono text-sm tracking-widest uppercase">
                Portal
              </Link>
            ) : (
              <Link href="/auth/login" onClick={() => setOpen(false)} className="text-cold-smoke font-mono text-sm tracking-widest uppercase">
                Login
              </Link>
            )}
          </div>
        </div>
      )}
    </nav>
  )
}
