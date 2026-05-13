import RoomCard from '@/components/hq/RoomCard'

const rooms = [
  { title: "Cold's Cannabis Club", subtitle: "Apparel, signals, drops, and gear from the edge.", href: '/ccc', icon: '🌿', delay: 0.1 },
  { title: 'The Store', subtitle: 'Official gear. Every drop means something.', href: '/store', icon: '🛒', delay: 0.15 },
  { title: 'Ice Bong Six', subtitle: 'Stoner gamers. No suits. No fake esports energy.', href: '/ib6', icon: '🎮', delay: 0.2 },
  { title: 'Cold Cartel', subtitle: 'Not everyone gets in. Not everyone needs to.', href: '/cartel', icon: '🃏', delay: 0.25 },
  { title: 'Cold Code', subtitle: 'Rules before rank. Loyalty before noise.', href: '/cold-code', icon: '📜', delay: 0.3 },
  { title: 'Broadcasts', subtitle: 'Table talks, field notes, and lore drops.', href: '/broadcasts', icon: '📻', delay: 0.35 },
  { title: 'Events', subtitle: 'The signal leaves the screen.', href: '/events', icon: '📍', delay: 0.4 },
  { title: 'Member Portal', subtitle: 'Your rank. Your missions. Your rewards.', href: '/portal', icon: '🔐', delay: 0.45 },
]

export default function HQPage() {
  return (
    <div className="min-h-screen bg-cold-black px-6 py-16">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">COLD EMPIRE</p>
          <h1 className="text-4xl lg:text-5xl font-mono text-cold-white mb-3">HQ</h1>
          <p className="text-cold-smoke font-mono text-lg">
            Choose your room. Every door leads somewhere.
          </p>
        </div>

        {/* Rooms grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {rooms.map((room) => (
            <RoomCard key={room.href} {...room} />
          ))}
        </div>

        {/* Status bar */}
        <div className="mt-16 border-t border-cold-gray/40 pt-8 flex items-center gap-3">
          <div className="w-2 h-2 bg-cold-green rounded-full animate-pulse" />
          <p className="text-cold-smoke font-mono text-xs tracking-widest uppercase">
            All systems operational — Cold Empire HQ
          </p>
        </div>
      </div>
    </div>
  )
}
