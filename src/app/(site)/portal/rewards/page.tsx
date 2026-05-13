import { getSession } from '@/lib/auth'
import { redirect } from 'next/navigation'
import { getRankById } from '@/data/ranks'

const rewards = [
  { id: 'rew_001', name: '10% Off Coupon', description: 'One-time use discount code for the store.', pointCost: 100, minRank: 'family-friend' },
  { id: 'rew_002', name: 'Early Drop Access', description: '48-hour early access to the next drop.', pointCost: 250, minRank: 'associate' },
  { id: 'rew_003', name: 'Exclusive Discord Role', description: 'Custom role in the Cold Empire Discord.', pointCost: 500, minRank: 'associate' },
  { id: 'rew_004', name: 'Cartel Consideration', description: 'Fast-track review for Cartel membership.', pointCost: 1000, minRank: 'lieutenant' },
  { id: 'rew_005', name: 'Limited Merch Drop', description: 'Access to a members-only product release.', pointCost: 750, minRank: 'lieutenant' },
  { id: 'rew_006', name: 'ARG Clue Package', description: 'A hidden clue delivered to your inbox.', pointCost: 300, minRank: 'associate' },
]

export default async function RewardsPage() {
  const session = await getSession()
  if (!session?.user) redirect('/auth/login')

  const userPoints = (session.user as { points?: number }).points ?? 0
  const userRank = (session.user as { rank?: string }).rank ?? 'prospect'
  const currentRank = getRankById(userRank)

  return (
    <div className="min-h-screen bg-cold-black px-6 lg:px-16 max-w-6xl mx-auto py-12">
      <div className="mb-8">
        <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-2">MEMBER PORTAL</p>
        <h1 className="text-3xl font-mono text-cold-white mb-2">Rewards</h1>
        <div className="flex items-center gap-4">
          <p className="text-cold-smoke font-mono text-sm">
            Available points: <span className="text-cold-green font-bold">{userPoints}</span>
          </p>
          {currentRank && (
            <p className="text-cold-smoke font-mono text-sm">
              Rank: <span style={{ color: currentRank.color }}>{currentRank.name}</span>
            </p>
          )}
        </div>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {rewards.map((reward) => {
          const canAfford = userPoints >= reward.pointCost
          return (
            <div key={reward.id} className={`border p-5 bg-cold-charcoal ${canAfford ? 'border-cold-gray/40 hover:border-cold-green/40' : 'border-cold-gray/20 opacity-60'} transition-all`}>
              <h3 className="text-cold-white font-mono text-sm mb-2">{reward.name}</h3>
              <p className="text-cold-smoke font-mono text-xs mb-4 leading-relaxed">{reward.description}</p>
              <div className="flex items-center justify-between mt-auto">
                <span className="text-cold-green font-mono text-sm">{reward.pointCost} pts</span>
                <button
                  disabled={!canAfford}
                  className="border border-cold-green text-cold-green font-mono text-xs tracking-widest uppercase px-4 py-2 hover:bg-cold-green hover:text-cold-black transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  {canAfford ? 'Redeem' : 'Not enough pts'}
                </button>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
