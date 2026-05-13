import { NextRequest, NextResponse } from 'next/server'
import { stripe } from '@/lib/stripe'

export async function POST(req: NextRequest) {
  try {
    const { items } = await req.json()

    if (!items || items.length === 0) {
      return NextResponse.json({ error: 'No items in cart' }, { status: 400 })
    }

    const lineItems = items.map((item: { name: string; price: number; qty: number; size: string; color: string }) => ({
      price_data: {
        currency: 'usd',
        product_data: {
          name: item.name,
          description: `${item.size} / ${item.color}`,
        },
        unit_amount: item.price,
      },
      quantity: item.qty,
    }))

    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      line_items: lineItems,
      success_url: `${process.env.NEXTAUTH_URL}/checkout/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.NEXTAUTH_URL}/checkout/cancel`,
      shipping_address_collection: { allowed_countries: ['US', 'CA'] },
      metadata: {
        items: JSON.stringify(items.map((i: { name: string; qty: number }) => ({ name: i.name, qty: i.qty }))),
      },
    })

    return NextResponse.json({ url: session.url })
  } catch (error) {
    console.error('Stripe checkout error:', error)
    return NextResponse.json({ error: 'Failed to create checkout session' }, { status: 500 })
  }
}
