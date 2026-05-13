'use client'

import { useRouter, useSearchParams } from 'next/navigation'
import { Suspense } from 'react'
import Doorman from '@/components/door/Doorman'
import { motion } from 'framer-motion'

function AgeGateContent() {
  const router = useRouter()
  const params = useSearchParams()
  const dest = params.get('dest') ?? '/hq'

  function handleYes() {
    document.cookie = 'cold_age=verified; max-age=2592000; path=/; SameSite=Lax'
    router.push(dest)
  }

  function handleNo() {
    router.push('/wrong-door')
  }

  return (
    <div className="min-h-screen bg-cold-black flex items-center justify-center px-6">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(0,255,65,0.02)_0%,transparent_70%)]" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative z-10 max-w-md w-full"
      >
        <Doorman message='"Before you keep walking, answer straight. Are you 21 or older?"'>
          <div className="flex gap-4 mt-6">
            <button
              onClick={handleYes}
              className="flex-1 border border-cold-green text-cold-green font-mono tracking-widest uppercase px-6 py-3 text-sm hover:bg-cold-green hover:text-cold-black transition-all"
            >
              Yes, I&apos;m 21+
            </button>
            <button
              onClick={handleNo}
              className="flex-1 border border-cold-gray text-cold-smoke font-mono tracking-widest uppercase px-6 py-3 text-sm hover:border-cold-gray-light hover:text-cold-white transition-all"
            >
              No
            </button>
          </div>
          <p className="text-cold-gray-light font-mono text-xs mt-4 leading-relaxed">
            Some areas of this site contain cannabis-related content for adults 21+. We take this seriously.
          </p>
        </Doorman>
      </motion.div>
    </div>
  )
}

export default function AgeGatePage() {
  return (
    <Suspense>
      <AgeGateContent />
    </Suspense>
  )
}
