'use client'

import { getProductBySlug, products, formatPrice } from '@/data/products'
import { notFound } from 'next/navigation'
import { useState } from 'react'
import { useCart } from '@/lib/cartContext'
import CartDrawer from '@/components/store/CartDrawer'
import Link from 'next/link'

export default function ProductPage({ params }: { params: { slug: string } }) {
  const productData = getProductBySlug(params.slug)
  if (!productData) notFound()
  // Safe to assert: notFound() throws above if undefined
  const product = productData!

  const { addItem } = useCart()
  const [size, setSize] = useState(product.sizes[0])
  const [color, setColor] = useState(product.colors[0])
  const [qty] = useState(1)
  const [cartOpen, setCartOpen] = useState(false)
  const [added, setAdded] = useState(false)

  function handleAdd() {
    addItem({ id: product.id, slug: product.slug, name: product.name, price: product.price, size, color, qty })
    setAdded(true)
    setCartOpen(true)
    setTimeout(() => setAdded(false), 2000)
  }

  const related = products.filter(
    (p) => p.id !== product.id && (p.collection === product.collection || p.tags.some((t) => product.tags.includes(t)))
  ).slice(0, 3)

  return (
    <div className="min-h-screen bg-cold-black px-6 lg:px-16 max-w-7xl mx-auto py-12">
      <div className="grid lg:grid-cols-2 gap-16 mb-20">
        {/* Image */}
        <div>
          <div className="aspect-square bg-cold-charcoal border border-cold-gray flex items-center justify-center">
            <span className="text-cold-smoke font-mono text-sm tracking-wide">[ PRODUCT IMAGE ]</span>
          </div>
        </div>

        {/* Details */}
        <div className="flex flex-col">
          <div className="mb-2">
            <Link href="/store" className="text-cold-smoke hover:text-cold-green font-mono text-xs tracking-widest uppercase transition-colors">← Store</Link>
          </div>

          <p className="text-cold-smoke font-mono text-xs tracking-widest uppercase mb-2">{product.collection}</p>
          <h1 className="text-3xl font-mono text-cold-white mb-3">{product.name}</h1>
          <p className="text-cold-green font-mono text-2xl mb-6">{formatPrice(product.price)}</p>

          <p className="text-cold-smoke font-mono text-sm leading-relaxed mb-8">{product.description}</p>

          {/* Lore note */}
          <div className="border-l-2 border-cold-green pl-4 mb-8">
            <p className="text-cold-white font-mono text-sm italic leading-relaxed">{product.loreNote}</p>
            <Link href="/cold-code" className="text-cold-green font-mono text-xs mt-2 inline-block hover:opacity-70 transition-opacity">
              What does this mean? →
            </Link>
          </div>

          {/* Size */}
          {product.sizes.length > 1 && (
            <div className="mb-6">
              <p className="text-cold-smoke font-mono text-xs tracking-widest uppercase mb-3">Size</p>
              <div className="flex flex-wrap gap-2">
                {product.sizes.map((s) => (
                  <button
                    key={s}
                    onClick={() => setSize(s)}
                    className={`font-mono text-xs px-4 py-2 border transition-all ${size === s ? 'border-cold-green bg-cold-green text-cold-black' : 'border-cold-gray text-cold-smoke hover:border-cold-green/50'}`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Color */}
          {product.colors.length > 1 && (
            <div className="mb-6">
              <p className="text-cold-smoke font-mono text-xs tracking-widest uppercase mb-3">Color</p>
              <div className="flex flex-wrap gap-2">
                {product.colors.map((c) => (
                  <button
                    key={c}
                    onClick={() => setColor(c)}
                    className={`font-mono text-xs px-4 py-2 border transition-all ${color === c ? 'border-cold-green bg-cold-green text-cold-black' : 'border-cold-gray text-cold-smoke hover:border-cold-green/50'}`}
                  >
                    {c}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Add to cart */}
          <button
            onClick={handleAdd}
            className="w-full bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase py-4 hover:opacity-90 transition-opacity mb-3 text-sm"
          >
            {added ? '✓ Added to Cart' : 'Add to Cart'}
          </button>

          <button
            onClick={() => setCartOpen(true)}
            className="w-full border border-cold-gray text-cold-smoke font-mono tracking-widest uppercase py-3 text-xs hover:border-cold-green/50 hover:text-cold-white transition-all"
          >
            View Cart
          </button>
        </div>
      </div>

      {/* Related products */}
      {related.length > 0 && (
        <div className="border-t border-cold-gray/40 pt-12">
          <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-6">Related Drops</p>
          <div className="grid sm:grid-cols-3 gap-4">
            {related.map((r) => (
              <Link key={r.id} href={`/store/${r.slug}`} className="group block">
                <div className="aspect-square bg-cold-charcoal border border-cold-gray group-hover:border-cold-green/50 mb-3 flex items-center justify-center transition-all">
                  <span className="text-cold-smoke font-mono text-xs">[ IMAGE ]</span>
                </div>
                <h3 className="text-cold-white group-hover:text-cold-green font-mono text-sm mb-1 transition-colors">{r.name}</h3>
                <p className="text-cold-green font-mono text-sm">{formatPrice(r.price)}</p>
              </Link>
            ))}
          </div>
        </div>
      )}

      {cartOpen && <CartDrawer onClose={() => setCartOpen(false)} />}
    </div>
  )
}
