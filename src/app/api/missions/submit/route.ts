import { NextRequest, NextResponse } from 'next/server'
import { db } from '@/lib/db'
import { getSession } from '@/lib/auth'

export async function POST(req: NextRequest) {
  const session = await getSession()
  if (!session?.user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  try {
    const { missionId, proof } = await req.json()
    const userId = (session.user as { id?: string }).id!

    const existing = await db.missionCompletion.findFirst({
      where: { userId, missionId, status: { not: 'rejected' } },
    })

    if (existing) {
      return NextResponse.json({ error: 'Mission already submitted' }, { status: 400 })
    }

    const completion = await db.missionCompletion.create({
      data: { userId, missionId, proof: proof ?? null, status: 'pending' },
    })

    return NextResponse.json({ success: true, id: completion.id })
  } catch {
    return NextResponse.json({ error: 'Server error' }, { status: 500 })
  }
}
