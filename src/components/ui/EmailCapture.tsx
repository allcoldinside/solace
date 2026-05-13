'use client'

import { useState } from 'react'

interface EmailCaptureProps {
  source?: string
  tags?: string
  placeholder?: string
  ctaText?: string
  successMessage?: string
}

export default function EmailCapture({
  source = 'site',
  tags = '',
  placeholder = 'your@email.com',
  ctaText = 'Get the Signal',
  successMessage = 'Signal received. Watch your inbox.',
}: EmailCaptureProps) {
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')
  const [msg, setMsg] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!email) return
    setStatus('loading')
    try {
      const res = await fetch('/api/email/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, source, tags }),
      })
      if (res.ok) {
        setStatus('success')
        setMsg(successMessage)
        setEmail('')
      } else {
        const data = await res.json()
        setStatus('error')
        setMsg(data.error ?? 'Something went wrong.')
      }
    } catch {
      setStatus('error')
      setMsg('Connection failed. Try again.')
    }
  }

  if (status === 'success') {
    return (
      <div className="border border-cold-green/40 bg-cold-green/5 p-4 text-cold-green font-mono text-sm tracking-wide">
        ✓ {msg}
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder={placeholder}
        required
        className="flex-1 bg-cold-charcoal border border-cold-gray text-cold-white font-mono px-4 py-3 text-sm focus:outline-none focus:border-cold-green transition-colors"
      />
      <button
        type="submit"
        disabled={status === 'loading'}
        className="bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase px-6 py-3 text-sm hover:opacity-90 transition-opacity disabled:opacity-50 whitespace-nowrap"
      >
        {status === 'loading' ? '...' : ctaText}
      </button>
      {status === 'error' && (
        <p className="text-cold-red text-xs font-mono mt-1 sm:col-span-2">{msg}</p>
      )}
    </form>
  )
}
