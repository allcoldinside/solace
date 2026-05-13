import type { Metadata } from 'next'
import '@/styles/globals.css'
import SessionWrapper from '@/components/layout/SessionWrapper'

export const metadata: Metadata = {
  title: 'Cold Empire',
  description:
    "You found the door. Cold's Cannabis Club. Ice Bong Six. Cold Cartel. GetHigh.life",
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
          {children}
        </SessionWrapper>
      </body>
    </html>
  )
}
