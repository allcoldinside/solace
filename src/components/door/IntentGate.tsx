'use client'

import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'

const choices = [
  { label: "I'm here for the gear", route: '/age-gate?dest=/ccc', desc: "Cold's Cannabis Club" },
  { label: "I'm here for the games", route: '/ib6', desc: 'Ice Bong Six — IB6 Lobby' },
  { label: 'I heard about the Cartel', route: '/age-gate?dest=/cartel', desc: 'Cold Cartel' },
]

export default function IntentGate() {
  const router = useRouter()

  function handleChoice(route: string) {
    if (typeof window !== 'undefined') {
      sessionStorage.setItem('cold_intent', route)
    }
    router.push(route)
  }

  return (
    <div className="flex flex-col gap-4 w-full max-w-sm">
      {choices.map((c, i) => (
        <motion.button
          key={c.label}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: i * 0.1 }}
          onClick={() => handleChoice(c.route)}
          className="group text-left border border-cold-gray/60 hover:border-cold-green/60 bg-cold-charcoal hover:bg-cold-green/5 p-4 transition-all duration-200"
        >
          <p className="text-cold-white group-hover:text-cold-green font-mono text-sm tracking-wide transition-colors">
            {c.label}
          </p>
          <p className="text-cold-smoke font-mono text-xs mt-1">{c.desc}</p>
        </motion.button>
      ))}

      <motion.button
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        onClick={() => handleChoice('/hq')}
        className="text-cold-smoke hover:text-cold-white font-mono text-xs tracking-widest uppercase transition-colors text-center pt-2"
      >
        I&apos;m just looking around →
      </motion.button>
    </div>
  )
}
