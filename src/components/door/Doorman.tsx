'use client'

import { motion } from 'framer-motion'

interface DoormanProps {
  message: string
  children?: React.ReactNode
}

export default function Doorman({ message, children }: DoormanProps) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -40 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className="flex flex-col items-start gap-4 max-w-sm"
    >
      {/* Doorman silhouette */}
      <div className="flex items-end gap-4">
        <div className="relative w-16 h-20">
          {/* Simple noir silhouette */}
          <svg viewBox="0 0 64 80" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full">
            {/* Fedora */}
            <ellipse cx="32" cy="18" rx="20" ry="4" fill="#00ff41" opacity="0.9" />
            <rect x="16" y="14" width="32" height="8" rx="2" fill="#00ff41" opacity="0.9" />
            {/* Head */}
            <circle cx="32" cy="28" r="10" fill="#1a1a1a" stroke="#00ff41" strokeWidth="0.5" />
            {/* Eyes */}
            <circle cx="28" cy="27" r="1.5" fill="#00ff41" />
            <circle cx="36" cy="27" r="1.5" fill="#00ff41" />
            {/* Body */}
            <path d="M18 40 Q32 36 46 40 L50 72 H14 L18 40Z" fill="#0f0f0f" stroke="#00ff41" strokeWidth="0.5" />
            {/* Coat lapels */}
            <path d="M32 40 L24 52 L32 50 L40 52 L32 40Z" fill="#1a1a1a" />
            {/* Arms */}
            <path d="M18 40 L10 60" stroke="#0f0f0f" strokeWidth="8" strokeLinecap="round" />
            <path d="M46 40 L54 58" stroke="#0f0f0f" strokeWidth="8" strokeLinecap="round" />
            {/* Cigarette */}
            <line x1="50" y1="56" x2="58" y2="53" stroke="#c9a84c" strokeWidth="2" />
            <circle cx="58" cy="52" r="1" fill="#ff6600" opacity="0.8" />
          </svg>
          {/* Glow */}
          <div className="absolute inset-0 bg-cold-green/5 rounded-full blur-xl" />
        </div>

        {/* Speech bubble */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.4 }}
          className="relative bg-cold-charcoal border border-cold-green/40 p-4 max-w-xs"
        >
          {/* Bubble tail */}
          <div className="absolute -left-2 bottom-4 w-0 h-0 border-t-4 border-t-transparent border-b-4 border-b-transparent border-r-8 border-r-cold-charcoal" />
          <p className="text-cold-white font-mono text-sm leading-relaxed">{message}</p>
        </motion.div>
      </div>

      {children && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.4 }}
          className="w-full"
        >
          {children}
        </motion.div>
      )}
    </motion.div>
  )
}
