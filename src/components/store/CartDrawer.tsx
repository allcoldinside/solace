'use client'

import { useCart } from '@/lib/cartContext'
import { formatPrice } from '@/data/products'
import { useState } from 'react'

export default function CartDrawer({ onClose }: { onClose: () => void }) {
  const { items, removeItem, updateQty, total } = useCart()
  const [loading, setLoading] = useState(false)

  async function handleCheckout() {
    setLoading(true)
    try {
      const res = await fetch('/api/stripe/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items }),
      })
      const data = await res.json()
      if (data.url) {
        window.location.href = data.url
      }
    } catch {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex">
      <div className="flex-1 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="w-full max-w-md bg-cold-dark border-l border-cold-gray/40 flex flex-col h-full">
        <div className="flex items-center justify-between px-6 py-4 border-b border-cold-gray/40">
          <h2 className="font-mono text-cold-white tracking-widest uppercase text-sm">Cart</h2>
          <button onClick={onClose} className="text-cold-smoke hover:text-cold-white transition-colors text-xl">×</button>
        </div>

        <div className="flex-1 overflow-y-auto px-6 py-4">
          {items.length === 0 ? (
            <p className="text-cold-smoke font-mono text-sm text-center mt-8">The cart is empty.</p>
          ) : (
            <div className="space-y-4">
              {items.map((item) => (
                <div key={`${item.id}-${item.size}-${item.color}`} className="flex gap-4 border-b border-cold-gray/40 pb-4">
                  <div className="w-16 h-16 bg-cold-charcoal flex items-center justify-center flex-shrink-0">
                    <span className="text-cold-smoke text-xs">IMG</span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-cold-white font-mono text-sm truncate">{item.name}</p>
                    <p className="text-cold-smoke font-mono text-xs">{item.size} / {item.color}</p>
                    <p className="text-cold-green font-mono text-sm mt-1">{formatPrice(item.price)}</p>
                    <div className="flex items-center gap-3 mt-2">
                      <button onClick={() => updateQty(item.id, item.size, item.color, item.qty - 1)} className="text-cold-smoke hover:text-cold-white w-6 h-6 border border-cold-gray/40 flex items-center justify-center font-mono text-sm">−</button>
                      <span className="text-cold-white font-mono text-sm w-4 text-center">{item.qty}</span>
                      <button onClick={() => updateQty(item.id, item.size, item.color, item.qty + 1)} className="text-cold-smoke hover:text-cold-white w-6 h-6 border border-cold-gray/40 flex items-center justify-center font-mono text-sm">+</button>
                      <button onClick={() => removeItem(item.id, item.size, item.color)} className="text-cold-smoke hover:text-red-400 font-mono text-xs ml-auto transition-colors">Remove</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {items.length > 0 && (
          <div className="px-6 py-4 border-t border-cold-gray/40">
            <div className="flex items-center justify-between mb-4">
              <p className="text-cold-smoke font-mono text-sm">Total</p>
              <p className="text-cold-white font-mono text-lg">{formatPrice(total)}</p>
            </div>
            <button
              onClick={handleCheckout}
              disabled={loading}
              className="w-full bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase py-4 hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {loading ? 'Redirecting...' : 'Checkout'}
            </button>
            <p className="text-cold-smoke font-mono text-xs text-center mt-3">
              Powered by Stripe — Secure checkout
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
