'use client'

import { motion } from 'framer-motion'

export default function DoorScene() {
  return (
    <div className="relative w-full h-full flex items-center justify-center">
      {/* Fog particles */}
      {[...Array(6)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute rounded-full pointer-events-none"
          style={{
            width: `${120 + i * 60}px`,
            height: `${60 + i * 30}px`,
            background: 'radial-gradient(ellipse, rgba(0,255,65,0.04) 0%, transparent 70%)',
            left: `${10 + i * 12}%`,
            top: `${40 + (i % 3) * 15}%`,
          }}
          animate={{
            x: [0, 30 + i * 10, 0],
            y: [0, -15 - i * 5, 0],
            opacity: [0.3, 0.6, 0.3],
          }}
          transition={{
            duration: 6 + i * 1.5,
            repeat: Infinity,
            ease: 'easeInOut',
            delay: i * 0.8,
          }}
        />
      ))}

      {/* Door SVG */}
      <motion.div
        className="relative"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 1.5, ease: 'easeOut' }}
      >
        <svg
          width="180"
          height="280"
          viewBox="0 0 180 280"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Door frame */}
          <rect x="2" y="2" width="176" height="276" fill="#0a0a0a" stroke="#1a1a1a" strokeWidth="3" />
          {/* Door panel */}
          <rect x="12" y="12" width="156" height="256" fill="#0f0f0f" stroke="#2a2a2a" strokeWidth="1" />
          {/* Door panels details */}
          <rect x="20" y="20" width="64" height="100" fill="none" stroke="#1f1f1f" strokeWidth="1" />
          <rect x="96" y="20" width="64" height="100" fill="none" stroke="#1f1f1f" strokeWidth="1" />
          <rect x="20" y="136" width="140" height="120" fill="none" stroke="#1f1f1f" strokeWidth="1" />
          {/* Doorknob */}
          <motion.circle
            cx="140"
            cy="145"
            r="8"
            fill="#1a1a1a"
            stroke="#00ff41"
            strokeWidth="1.5"
            animate={{
              boxShadow: ['0 0 5px rgba(0,255,65,0.3)', '0 0 15px rgba(0,255,65,0.8)', '0 0 5px rgba(0,255,65,0.3)'],
            }}
          />
          <circle cx="140" cy="145" r="4" fill="#00cc33" opacity="0.7" />
          {/* Neon glow around door */}
          <rect x="2" y="2" width="176" height="276" fill="none" stroke="#00ff41" strokeWidth="0.5" opacity="0.3" />
        </svg>

        {/* Glow effect behind door */}
        <motion.div
          className="absolute inset-0 pointer-events-none"
          style={{
            background: 'radial-gradient(ellipse at center, rgba(0,255,65,0.08) 0%, transparent 70%)',
          }}
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
        />
      </motion.div>
    </div>
  )
}
