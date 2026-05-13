import { NextRequest, NextResponse } from 'next/server'
import { stripe } from '@/lib/stripe'
import { db } from '@/lib/db'
import { sendOrderConfirmEmail } from '@/lib/email'
import Stripe from 'stripe'

export async function POST(req: NextRequest) {
  const body = await req.text()
  const signature = req.headers.get('stripe-signature')!

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET!)
  } catch {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 })
  }

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object as Stripe.Checkout.Session

    try {
      const items = session.metadata?.items ?? '[]'
      const email = session.customer_details?.email ?? ''

      await db.order.create({
        data: {
          stripeSessionId: session.id,
          amount: session.amount_total ?? 0,
          status: 'paid',
          items,
          email,
        },
      })

      if (email) {
        await sendOrderConfirmEmail(email, items)
        await db.emailSubscriber.upsert({
          where: { email },
          create: { email, source: 'checkout', tags: 'customer' },
          update: {},
        })
      }
    } catch (err) {
      console.error('Webhook DB error:', err)
    }
  }

  return NextResponse.json({ received: true })
}
