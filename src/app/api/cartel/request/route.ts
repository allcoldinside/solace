import { NextRequest, NextResponse } from 'next/server'
import { db } from '@/lib/db'
import { sendCartelRequestEmail } from '@/lib/email'

export async function POST(req: NextRequest) {
  try {
    const { email, alias, interest, discord } = await req.json()

    if (!email || !email.includes('@')) {
      return NextResponse.json({ error: 'Valid email required' }, { status: 400 })
    }

    await db.cartelRequest.create({
      data: { email, alias: alias ?? null, interest: interest ?? null, discord: discord ?? null },
    })

    await db.emailSubscriber.upsert({
      where: { email },
      create: { email, source: 'cartel-request', tags: 'cartel,prospect' },
      update: {},
    })

    await sendCartelRequestEmail(email)

    return NextResponse.json({ success: true })
  } catch {
    return NextResponse.json({ error: 'Server error' }, { status: 500 })
  }
}
