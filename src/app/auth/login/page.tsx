'use client'

import { useState } from 'react'
import { signIn } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function LoginPage() {
  const router = useRouter()
  const [form, setForm] = useState({ email: '', password: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')

    const result = await signIn('credentials', {
      email: form.email,
      password: form.password,
      redirect: false,
    })

    if (result?.ok) {
      router.push('/portal')
    } else {
      setError('Invalid credentials.')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-cold-black flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        <div className="mb-8">
          <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">COLD EMPIRE</p>
          <h1 className="text-3xl font-mono text-cold-white mb-2">Welcome Back</h1>
          <p className="text-cold-smoke font-mono text-sm">The door recognizes you.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-cold-smoke font-mono text-xs tracking-wide mb-2">EMAIL</label>
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
            <label className="block text-cold-smoke font-mono text-xs tracking-wide mb-2">PASSWORD</label>
            <input
              type="password"
              required
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="w-full bg-cold-charcoal border border-cold-gray text-cold-white font-mono px-4 py-3 text-sm focus:outline-none focus:border-cold-green transition-colors"
              placeholder="Your password"
            />
          </div>

          {error && <p className="text-red-400 font-mono text-xs">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase py-4 hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {loading ? '...' : 'Enter'}
          </button>
        </form>

        <p className="text-cold-smoke font-mono text-xs mt-6 text-center">
          No account?{' '}
          <Link href="/auth/register" className="text-cold-green hover:opacity-70 transition-opacity">
            Register
          </Link>
        </p>
      </div>
    </div>
  )
}
