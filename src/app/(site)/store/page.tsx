'use client'

import { useState } from 'react'
import { products, getCollections, formatPrice } from '@/data/products'
import Link from 'next/link'
import { useCart } from '@/lib/cartContext'
import CartDrawer from '@/components/store/CartDrawer'

const collections = getCollections()

export default function StorePage() {
  const [activeCollection, setActiveCollection] = useState<string | null>(null)
  const [cartOpen, setCartOpen] = useState(false)
  const { count } = useCart()

  const filtered = activeCollection
    ? products.filter((p) => p.collection === activeCollection && p.inStock)
    : products.filter((p) => p.inStock)

  return (
    <div className="min-h-screen bg-cold-black">
      {/* Store header */}
      <div className="border-b border-cold-gray/40 px-6 lg:px-16 py-8 max-w-7xl mx-auto">
        <div className="flex items-end justify-between">
          <div>
            <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-2">COLD EMPIRE</p>
            <h1 className="text-4xl font-mono text-cold-white">The Store</h1>
            <p className="text-cold-smoke font-mono text-sm mt-2">Official gear from the cold side.</p>
          </div>
          <button
            onClick={() => setCartOpen(true)}
            className="relative border border-cold-gray hover:border-cold-green text-cold-white font-mono text-sm tracking-widest uppercase px-4 py-2 transition-all"
          >
            Cart
            {count > 0 && (
              <span className="absolute -top-2 -right-2 w-5 h-5 bg-cold-green text-cold-black text-xs font-mono flex items-center justify-center rounded-full">
                {count}
              </span>
            )}
          </button>
        </div>

        {/* Collections filter */}
        <div className="flex flex-wrap gap-2 mt-6">
          <button
            onClick={() => setActiveCollection(null)}
            className={`font-mono text-xs tracking-widest uppercase px-3 py-1.5 border transition-all ${!activeCollection ? 'border-cold-green bg-cold-green text-cold-black' : 'border-cold-gray text-cold-smoke hover:border-cold-green/50 hover:text-cold-white'}`}
          >
            All
          </button>
          {collections.map((c) => (
            <button
              key={c}
              onClick={() => setActiveCollection(c === activeCollection ? null : c)}
              className={`font-mono text-xs tracking-widest uppercase px-3 py-1.5 border transition-all ${activeCollection === c ? 'border-cold-green bg-cold-green text-cold-black' : 'border-cold-gray text-cold-smoke hover:border-cold-green/50 hover:text-cold-white'}`}
            >
              {c}
            </button>
          ))}
        </div>
      </div>

      {/* Grid */}
      <div className="max-w-7xl mx-auto px-6 lg:px-16 py-10">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {filtered.map((product) => (
            <Link key={product.id} href={`/store/${product.slug}`} className="group block">
              <div className="aspect-square bg-cold-charcoal border border-cold-gray group-hover:border-cold-green/50 mb-3 flex items-center justify-center relative overflow-hidden transition-all">
                <span className="text-cold-smoke font-mono text-xs tracking-wide">[ IMAGE ]</span>
                <div className="absolute inset-0 bg-cold-green/0 group-hover:bg-cold-green/3 transition-all duration-300" />
              </div>
              <div className="px-1">
                <p className="text-cold-smoke font-mono text-xs tracking-wide mb-1">{product.collection}</p>
                <h3 className="text-cold-white group-hover:text-cold-green font-mono text-sm mb-1 transition-colors leading-tight">{product.name}</h3>
                <p className="text-cold-green font-mono text-sm">{formatPrice(product.price)}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {cartOpen && <CartDrawer onClose={() => setCartOpen(false)} />}
    </div>
  )
}
