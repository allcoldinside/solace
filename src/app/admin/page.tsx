import { requireAdmin } from '@/lib/auth'
import { redirect } from 'next/navigation'
import { db } from '@/lib/db'
import Link from 'next/link'

export default async function AdminPage() {
  const session = await requireAdmin()
  if (!session) redirect('/auth/login')

  const [
    memberCount,
    orderCount,
    subscriberCount,
    cartelRequests,
    pendingMissions,
    recentOrders,
    recentMembers,
  ] = await Promise.all([
    db.user.count(),
    db.order.count(),
    db.emailSubscriber.count(),
    db.cartelRequest.findMany({ where: { status: 'pending' }, orderBy: { createdAt: 'desc' }, take: 10 }),
    db.missionCompletion.findMany({ where: { status: 'pending' }, include: { user: true }, orderBy: { createdAt: 'desc' }, take: 10 }),
    db.order.findMany({ orderBy: { createdAt: 'desc' }, take: 10 }),
    db.user.findMany({ orderBy: { createdAt: 'desc' }, take: 10 }),
  ])

  const revenue = await db.order.aggregate({ _sum: { amount: true }, where: { status: 'paid' } })

  return (
    <div className="min-h-screen bg-cold-black px-6 lg:px-16 max-w-7xl mx-auto py-12">
      <div className="mb-8">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-2">COLD EMPIRE</p>
        <h1 className="text-3xl font-mono text-cold-white mb-1">Control Room</h1>
        <p className="text-cold-smoke font-mono text-sm">Admin Dashboard — Restricted Access</p>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Members', value: memberCount },
          { label: 'Orders', value: orderCount },
          { label: 'Subscribers', value: subscriberCount },
          { label: 'Revenue', value: `$${((revenue._sum.amount ?? 0) / 100).toFixed(2)}` },
        ].map((stat) => (
          <div key={stat.label} className="border border-cold-gray/40 bg-cold-charcoal p-5 text-center">
            <p className="text-cold-green font-mono text-2xl font-bold">{stat.value}</p>
            <p className="text-cold-smoke font-mono text-xs tracking-widest uppercase mt-1">{stat.label}</p>
          </div>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-6 mb-6">
        {/* Cartel request queue */}
        <div className="border border-cold-gray/40 bg-cold-charcoal p-5">
          <div className="flex items-center justify-between mb-4">
            <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono">Cartel Requests</p>
            <span className="bg-cold-green text-cold-black font-mono text-xs px-2 py-0.5">{cartelRequests.length}</span>
          </div>
          {cartelRequests.length === 0 ? (
            <p className="text-cold-smoke font-mono text-xs">No pending requests.</p>
          ) : (
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {cartelRequests.map((req) => (
                <div key={req.id} className="border border-cold-gray/40 p-3 flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="text-cold-white font-mono text-xs truncate">{req.email}</p>
                    <p className="text-cold-smoke font-mono text-xs">{req.alias ?? '—'} · {req.interest ?? '—'}</p>
                    <p className="text-cold-smoke font-mono text-xs">{new Date(req.createdAt).toLocaleDateString()}</p>
                  </div>
                  <div className="flex gap-2 flex-shrink-0">
                    <button className="border border-cold-green text-cold-green font-mono text-xs px-2 py-1 hover:bg-cold-green hover:text-cold-black transition-all">✓</button>
                    <button className="border border-cold-gray text-cold-smoke font-mono text-xs px-2 py-1 hover:border-red-500 hover:text-red-400 transition-all">✗</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Mission submission queue */}
        <div className="border border-cold-gray/40 bg-cold-charcoal p-5">
          <div className="flex items-center justify-between mb-4">
            <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono">Pending Missions</p>
            <span className="bg-cold-green text-cold-black font-mono text-xs px-2 py-0.5">{pendingMissions.length}</span>
          </div>
          {pendingMissions.length === 0 ? (
            <p className="text-cold-smoke font-mono text-xs">No pending mission submissions.</p>
          ) : (
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {pendingMissions.map((m) => (
                <div key={m.id} className="border border-cold-gray/40 p-3 flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="text-cold-white font-mono text-xs">{m.user.email}</p>
                    <p className="text-cold-smoke font-mono text-xs">{m.missionId}</p>
                    {m.proof && <p className="text-cold-smoke font-mono text-xs truncate">{m.proof}</p>}
                  </div>
                  <div className="flex gap-2 flex-shrink-0">
                    <button className="border border-cold-green text-cold-green font-mono text-xs px-2 py-1 hover:bg-cold-green hover:text-cold-black transition-all">✓</button>
                    <button className="border border-cold-gray text-cold-smoke font-mono text-xs px-2 py-1 hover:border-red-500 hover:text-red-400 transition-all">✗</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Recent orders */}
      <div className="border border-cold-gray/40 bg-cold-charcoal p-5 mb-6">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">Recent Orders</p>
        <div className="overflow-x-auto">
          <table className="w-full font-mono text-xs">
            <thead>
              <tr className="text-left text-cold-smoke border-b border-cold-gray/40">
                <th className="pb-2 pr-4">Date</th>
                <th className="pb-2 pr-4">Email</th>
                <th className="pb-2 pr-4">Amount</th>
                <th className="pb-2">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-cold-gray/20">
              {recentOrders.map((order) => (
                <tr key={order.id}>
                  <td className="py-2 pr-4 text-cold-smoke">{new Date(order.createdAt).toLocaleDateString()}</td>
                  <td className="py-2 pr-4 text-cold-white truncate max-w-[200px]">{order.email ?? '—'}</td>
                  <td className="py-2 pr-4 text-cold-green">${(order.amount / 100).toFixed(2)}</td>
                  <td className="py-2">
                    <span className={`border px-2 py-0.5 ${order.status === 'paid' ? 'border-cold-green/40 text-cold-green' : 'border-cold-gray/40 text-cold-smoke'}`}>
                      {order.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recent members */}
      <div className="border border-cold-gray/40 bg-cold-charcoal p-5">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">Recent Members</p>
        <div className="overflow-x-auto">
          <table className="w-full font-mono text-xs">
            <thead>
              <tr className="text-left text-cold-smoke border-b border-cold-gray/40">
                <th className="pb-2 pr-4">Joined</th>
                <th className="pb-2 pr-4">Email</th>
                <th className="pb-2 pr-4">Alias</th>
                <th className="pb-2 pr-4">Rank</th>
                <th className="pb-2">Points</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-cold-gray/20">
              {recentMembers.map((member) => (
                <tr key={member.id}>
                  <td className="py-2 pr-4 text-cold-smoke">{new Date(member.createdAt).toLocaleDateString()}</td>
                  <td className="py-2 pr-4 text-cold-white truncate max-w-[200px]">{member.email}</td>
                  <td className="py-2 pr-4 text-cold-smoke">{member.alias ?? '—'}</td>
                  <td className="py-2 pr-4 text-cold-green">{member.rank}</td>
                  <td className="py-2 text-cold-white">{member.points}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
