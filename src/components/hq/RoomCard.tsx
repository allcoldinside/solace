'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'

interface RoomCardProps {
  title: string
  subtitle: string
  href: string
  icon: string
  delay?: number
}

export default function RoomCard({ title, subtitle, href, icon, delay = 0 }: RoomCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5 }}
      whileHover={{ scale: 1.02 }}
    >
      <Link
        href={href}
        className="group block bg-cold-charcoal border border-cold-gray hover:border-cold-green/60 p-6 h-full transition-all duration-300 relative overflow-hidden"
      >
        {/* Hover glow */}
        <div className="absolute inset-0 bg-cold-green/0 group-hover:bg-cold-green/3 transition-all duration-300" />

        <div className="relative z-10">
          <div className="text-3xl mb-3">{icon}</div>
          <h2 className="text-cold-white group-hover:text-cold-green font-mono text-lg tracking-wide transition-colors mb-1">
            {title}
          </h2>
          <p className="text-cold-smoke font-mono text-xs leading-relaxed">{subtitle}</p>
          <p className="text-cold-green/50 group-hover:text-cold-green font-mono text-xs mt-4 tracking-widest uppercase transition-colors">
            Enter →
          </p>
        </div>

        {/* Corner accent */}
        <div className="absolute top-0 right-0 w-8 h-8 border-r border-t border-cold-green/0 group-hover:border-cold-green/40 transition-colors duration-300" />
      </Link>
    </motion.div>
  )
}
