import { NextRequest, NextResponse } from 'next/server'
import bcrypt from 'bcryptjs'
import { db } from '@/lib/db'

export async function POST(req: NextRequest) {
  try {
    const { email, alias, password } = await req.json()

    if (!email || !password || password.length < 8) {
      return NextResponse.json({ error: 'Email and password (min 8 chars) required.' }, { status: 400 })
    }

    const existing = await db.user.findUnique({ where: { email } })
    if (existing) {
      return NextResponse.json({ error: 'Account already exists.' }, { status: 409 })
    }

    const hashed = await bcrypt.hash(password, 12)

    await db.user.create({
      data: { email, alias: alias || null, password: hashed },
    })

    await db.emailSubscriber.upsert({
      where: { email },
      create: { email, source: 'register', tags: 'member' },
      update: {},
    })

    return NextResponse.json({ success: true })
  } catch {
    return NextResponse.json({ error: 'Server error' }, { status: 500 })
  }
}
