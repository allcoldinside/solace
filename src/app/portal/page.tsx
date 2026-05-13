import { getSession } from '@/lib/auth'
import { redirect } from 'next/navigation'
import { db } from '@/lib/db'
import { getRankById, getNextRank } from '@/data/ranks'
import { getActiveMissions } from '@/data/missions'
import Link from 'next/link'

export default async function PortalPage() {
  const session = await getSession()
  if (!session?.user) redirect('/auth/login')

  const userId = (session.user as { id?: string }).id!
  const user = await db.user.findUnique({
    where: { id: userId },
    include: { missions: true, rewards: true, orders: { take: 5, orderBy: { createdAt: 'desc' } } },
  })

  if (!user) redirect('/auth/login')

  const currentRank = getRankById(user.rank) ?? getRankById('prospect')!
  const nextRank = getNextRank(user.rank)
  const activeMissions = getActiveMissions().slice(0, 4)
  const completedMissionIds = user.missions.filter((m) => m.status === 'approved').map((m) => m.missionId)
  const pendingMissions = user.missions.filter((m) => m.status === 'pending')

  const progress = nextRank
    ? Math.min(100, Math.round((user.points / nextRank.pointsRequired) * 100))
    : 100

  return (
    <div className="min-h-screen bg-cold-black px-6 lg:px-16 max-w-7xl mx-auto py-12">
      {/* Welcome */}
      <div className="mb-10">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-2">MEMBER PORTAL</p>
        <h1 className="text-3xl font-mono text-cold-white">
          Welcome back, <span className="text-cold-green">{user.alias ?? user.email.split('@')[0]}</span>.
        </h1>
      </div>

      <div className="grid lg:grid-cols-3 gap-6 mb-8">
        {/* Rank card */}
        <div className="lg:col-span-1 border border-cold-gray/40 bg-cold-charcoal p-6">
          <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">Your Rank</p>
          <div
            className="text-2xl font-mono mb-1"
            style={{ color: currentRank.color }}
          >
            {currentRank.name}
          </div>
          <p className="text-cold-smoke font-mono text-xs mb-4 leading-relaxed">{currentRank.description}</p>

          <div className="mb-3">
            <div className="flex justify-between text-xs font-mono text-cold-smoke mb-1">
              <span>{user.points} pts</span>
              {nextRank && <span>{nextRank.pointsRequired} pts for {nextRank.name}</span>}
            </div>
            <div className="h-1.5 bg-cold-dark rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-500"
                style={{ width: `${progress}%`, background: currentRank.color }}
              />
            </div>
          </div>

          {nextRank && (
            <p className="text-cold-smoke font-mono text-xs">
              Next rank: <span className="text-cold-white">{nextRank.name}</span>
            </p>
          )}
        </div>

        {/* Stats */}
        <div className="lg:col-span-2 grid grid-cols-2 sm:grid-cols-4 gap-4">
          {[
            { label: 'Points', value: user.points.toLocaleString() },
            { label: 'Missions', value: completedMissionIds.length },
            { label: 'Orders', value: user.orders.length },
            { label: 'Rank Level', value: currentRank.level },
          ].map((stat) => (
            <div key={stat.label} className="border border-cold-gray/40 bg-cold-charcoal p-4 text-center">
              <p className="text-cold-green font-mono text-2xl font-bold">{stat.value}</p>
              <p className="text-cold-smoke font-mono text-xs tracking-widest uppercase mt-1">{stat.label}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Missions */}
        <div className="border border-cold-gray/40 bg-cold-charcoal p-6">
          <div className="flex items-center justify-between mb-4">
            <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono">Active Missions</p>
            <Link href="/portal/missions" className="text-cold-green font-mono text-xs hover:opacity-70 transition-opacity">
              View All →
            </Link>
          </div>
          <div className="space-y-3">
            {activeMissions.map((mission) => {
              const done = completedMissionIds.includes(mission.id)
              const pending = pendingMissions.some((m) => m.missionId === mission.id)
              return (
                <div key={mission.id} className="flex items-start gap-3 p-3 border border-cold-gray/40">
                  <div className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${done ? 'bg-cold-green' : pending ? 'bg-cold-gold' : 'bg-cold-gray'}`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-cold-white font-mono text-sm">{mission.title}</p>
                    <p className="text-cold-smoke font-mono text-xs">{mission.points} pts</p>
                  </div>
                  <span className={`text-xs font-mono px-2 py-0.5 border flex-shrink-0 ${done ? 'border-cold-green/40 text-cold-green' : pending ? 'border-cold-gold/40 text-cold-gold' : 'border-cold-gray/40 text-cold-smoke'}`}>
                    {done ? 'Done' : pending ? 'Pending' : 'Open'}
                  </span>
                </div>
              )
            })}
          </div>
        </div>

        {/* Recent Orders */}
        <div className="border border-cold-gray/40 bg-cold-charcoal p-6">
          <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">Recent Orders</p>
          {user.orders.length === 0 ? (
            <div className="text-center py-6">
              <p className="text-cold-smoke font-mono text-sm mb-4">No orders yet.</p>
              <Link href="/store" className="text-cold-green font-mono text-xs tracking-widest uppercase hover:opacity-70 transition-opacity">
                Shop the Drop →
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {user.orders.map((order) => (
                <div key={order.id} className="flex items-center justify-between p-3 border border-cold-gray/40">
                  <div>
                    <p className="text-cold-white font-mono text-xs">{new Date(order.createdAt).toLocaleDateString()}</p>
                    <p className="text-cold-smoke font-mono text-xs">{order.status}</p>
                  </div>
                  <p className="text-cold-green font-mono text-sm">${(order.amount / 100).toFixed(2)}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Perks */}
      <div className="mt-6 border border-cold-gray/40 bg-cold-charcoal p-6">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">Your Rank Perks — {currentRank.name}</p>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-2">
          {currentRank.perks.map((perk) => (
            <div key={perk} className="flex items-center gap-2 text-cold-white font-mono text-xs">
              <span className="text-cold-green">✓</span> {perk}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
