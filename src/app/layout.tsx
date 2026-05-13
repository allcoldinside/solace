import type { Metadata } from 'next'
import '@/styles/globals.css'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import ColdLogicBot from '@/components/cold-logic/ColdLogicBot'
import SessionWrapper from '@/components/layout/SessionWrapper'
import { CartProvider } from '@/lib/cartContext'

export const metadata: Metadata = {
  title: 'Cold Empire',
  description:
    'You found the door. Cold\'s Cannabis Club. Ice Bong Six. Cold Cartel. GetHigh.life',
  openGraph: {
    title: 'Cold Empire',
    description: 'You found the door. Most people walk past it.',
    siteName: 'Cold Empire',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <SessionWrapper>
          <CartProvider>
            <Navbar />
            <main className="pt-14">{children}</main>
            <Footer />
            <ColdLogicBot />
          </CartProvider>
        </SessionWrapper>
      </body>
    </html>
  )
}
