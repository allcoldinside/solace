'use client'

import { useState } from 'react'
import { signIn } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function RegisterPage() {
  const router = useRouter()
  const [form, setForm] = useState({ email: '', alias: '', password: '', confirm: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (form.password !== form.confirm) {
      setError('Passwords do not match.')
      return
    }
    setLoading(true)
    setError('')

    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: form.email, alias: form.alias, password: form.password }),
      })
      const data = await res.json()
      if (!res.ok) {
        setError(data.error ?? 'Registration failed.')
        setLoading(false)
        return
      }
      const result = await signIn('credentials', { email: form.email, password: form.password, redirect: false })
      if (result?.ok) {
        router.push('/portal')
      } else {
        router.push('/auth/login')
      }
    } catch {
      setError('Connection failed.')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-cold-black flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        <div className="mb-8">
          <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">COLD EMPIRE</p>
          <h1 className="text-3xl font-mono text-cold-white mb-2">Create Account</h1>
          <p className="text-cold-smoke font-mono text-sm">The door opens when you step in.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-cold-smoke font-mono text-xs tracking-wide mb-2">EMAIL *</label>
            <input
              type="email"
              required
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="w-full bg-cold-charcoal border border-cold-gray text-cold-white font-mono px-4 py-3 text-sm focus:outline-none focus:border-cold-green transition-colors"
              placeholder="your@email.com"
            />
          </div>
          <div>
            <label className="block text-cold-smoke font-mono text-xs tracking-wide mb-2">ALIAS (optional)</label>
            <input
              type="text"
              value={form.alias}
              onChange={(e) => setForm({ ...form, alias: e.target.value })}
              className="w-full bg-cold-charcoal border border-cold-gray text-cold-white font-mono px-4 py-3 text-sm focus:outline-none focus:border-cold-green transition-colors"
              placeholder="What should we call you?"
            />
          </div>
          <div>
            <label className="block text-cold-smoke font-mono text-xs tracking-wide mb-2">PASSWORD *</label>
            <input
              type="password"
              required
              minLength={8}
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="w-full bg-cold-charcoal border border-cold-gray text-cold-white font-mono px-4 py-3 text-sm focus:outline-none focus:border-cold-green transition-colors"
              placeholder="Minimum 8 characters"
            />
          </div>
          <div>
            <label className="block text-cold-smoke font-mono text-xs tracking-wide mb-2">CONFIRM PASSWORD *</label>
            <input
              type="password"
              required
              value={form.confirm}
              onChange={(e) => setForm({ ...form, confirm: e.target.value })}
              className="w-full bg-cold-charcoal border border-cold-gray text-cold-white font-mono px-4 py-3 text-sm focus:outline-none focus:border-cold-green transition-colors"
              placeholder="Repeat password"
            />
          </div>

          {error && <p className="text-red-400 font-mono text-xs">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase py-4 hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {loading ? '...' : 'Create Account'}
          </button>
        </form>

        <p className="text-cold-smoke font-mono text-xs mt-6 text-center">
          Already have an account?{' '}
          <Link href="/auth/login" className="text-cold-green hover:opacity-70 transition-opacity">
            Login
          </Link>
        </p>
      </div>
    </div>
  )
}
