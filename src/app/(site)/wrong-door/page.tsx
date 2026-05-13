import Link from 'next/link'

export default function WrongDoorPage() {
  return (
    <div className="min-h-screen bg-cold-black flex items-center justify-center px-6 text-center">
      <div>
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">ACCESS DENIED</p>
        <h1 className="text-3xl font-mono text-cold-white mb-3">Wrong door, kid.</h1>
        <p className="text-cold-smoke font-mono mb-8">
          Come back when the calendar says you can.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/ib6"
            className="border border-cold-green text-cold-green font-mono tracking-widest uppercase px-6 py-3 text-sm hover:bg-cold-green hover:text-cold-black transition-all"
          >
            Go to IB6 Gaming
          </Link>
          <Link
            href="/store?tag=general"
            className="border border-cold-gray text-cold-smoke font-mono tracking-widest uppercase px-6 py-3 text-sm hover:border-cold-gray-light hover:text-cold-white transition-all"
          >
            View General Apparel
          </Link>
        </div>
      </div>
    </div>
  )
}
