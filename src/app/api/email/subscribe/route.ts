import { NextRequest, NextResponse } from 'next/server'
import { db } from '@/lib/db'
import { sendWelcomeEmail } from '@/lib/email'

export async function POST(req: NextRequest) {
  try {
    const { email, source = 'site', tags = '' } = await req.json()

    if (!email || !email.includes('@')) {
      return NextResponse.json({ error: 'Valid email required' }, { status: 400 })
    }

    const existing = await db.emailSubscriber.findUnique({ where: { email } })

    if (!existing) {
      await db.emailSubscriber.create({ data: { email, source, tags } })
      await sendWelcomeEmail(email)
    }

    return NextResponse.json({ success: true })
  } catch {
    return NextResponse.json({ error: 'Server error' }, { status: 500 })
  }
}
