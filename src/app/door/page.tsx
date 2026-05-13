'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import DoorScene from '@/components/door/DoorScene'
import Doorman from '@/components/door/Doorman'
import IntentGate from '@/components/door/IntentGate'

type Stage = 'intro' | 'knock' | 'doorman' | 'intent'

export default function DoorPage() {
  const [stage, setStage] = useState<Stage>('intro')

  function handleKnock() {
    setStage('knock')
    setTimeout(() => setStage('doorman'), 800)
    setTimeout(() => setStage('intent'), 2200)
  }

  return (
    <div className="min-h-screen bg-cold-black flex items-center justify-center overflow-hidden relative">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(0,255,65,0.03)_0%,transparent_70%)]" />

      <div className="relative z-10 flex flex-col lg:flex-row items-center gap-12 lg:gap-20 px-6 max-w-5xl w-full">

        {/* Door visual */}
        <div className="w-48 h-72 lg:w-64 lg:h-96 flex-shrink-0">
          <DoorScene />
        </div>

        {/* Content */}
        <div className="flex flex-col items-start gap-8 max-w-md">
          <AnimatePresence mode="wait">
            {stage === 'intro' && (
              <motion.div
                key="intro"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.8 }}
                className="flex flex-col gap-6"
              >
                <div>
                  <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">
                    COLD EMPIRE
                  </p>
                  <h1 className="text-3xl lg:text-4xl font-mono text-cold-white leading-tight">
                    You found the door.
                  </h1>
                  <p className="text-cold-smoke font-mono text-lg mt-3">
                    Most people walk past it.
                  </p>
                </div>

                <button
                  onClick={handleKnock}
                  className="group relative border border-cold-green text-cold-green font-mono tracking-widest uppercase px-8 py-4 text-sm hover:bg-cold-green hover:text-cold-black transition-all duration-300"
                  style={{ boxShadow: '0 0 10px rgba(0,255,65,0.2)' }}
                >
                  <span className="relative z-10">Knock</span>
                  <div className="absolute inset-0 bg-cold-green opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                </button>
              </motion.div>
            )}

            {stage === 'knock' && (
              <motion.div
                key="knock"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col gap-3"
              >
                <motion.p
                  className="text-cold-green font-mono text-sm tracking-widest"
                  animate={{ opacity: [1, 0.4, 1] }}
                  transition={{ duration: 0.3, repeat: 2 }}
                >
                  *knock knock*
                </motion.p>
                <p className="text-cold-smoke font-mono text-xs tracking-wide">...</p>
              </motion.div>
            )}

            {(stage === 'doorman' || stage === 'intent') && (
              <motion.div key="doorman" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <Doorman message={`"Easy. Before you come inside, I gotta know what kind of trouble you're looking for."`}>
                  {stage === 'intent' && <IntentGate />}
                </Doorman>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Subtle scanline effect */}
      <div
        className="absolute inset-0 pointer-events-none opacity-5"
        style={{
          backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,255,65,0.1) 2px, rgba(0,255,65,0.1) 4px)',
        }}
      />
    </div>
  )
}
