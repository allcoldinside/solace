import { NextRequest, NextResponse } from 'next/server'
import { requireAdmin } from '@/lib/auth'
import { db } from '@/lib/db'
import { getMissionById } from '@/data/missions'

export async function PATCH(req: NextRequest) {
  const session = await requireAdmin()
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  try {
    const { id, status } = await req.json()

    const completion = await db.missionCompletion.findUnique({ where: { id } })
    if (!completion) return NextResponse.json({ error: 'Not found' }, { status: 404 })

    await db.missionCompletion.update({ where: { id }, data: { status } })

    if (status === 'approved') {
      const mission = getMissionById(completion.missionId)
      if (mission) {
        await db.user.update({
          where: { id: completion.userId },
          data: { points: { increment: mission.points } },
        })
      }
    }

    return NextResponse.json({ success: true })
  } catch {
    return NextResponse.json({ error: 'Server error' }, { status: 500 })
  }
}
