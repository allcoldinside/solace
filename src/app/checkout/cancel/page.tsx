import Link from 'next/link'

export default function CheckoutCancelPage() {
  return (
    <div className="min-h-screen bg-cold-black flex flex-col items-center justify-center px-6 text-center">
      <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">CHECKOUT CANCELLED</p>
      <h1 className="text-3xl font-mono text-cold-white mb-4">Transaction cancelled.</h1>
      <p className="text-cold-smoke font-mono mb-8">Your cart is still waiting.</p>
      <Link href="/store" className="bg-cold-green text-cold-black font-mono font-bold tracking-widest uppercase px-8 py-4 hover:opacity-90 transition-opacity">
        Return to Store
      </Link>
    </div>
  )
}
