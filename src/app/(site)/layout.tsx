import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import ColdLogicBot from '@/components/cold-logic/ColdLogicBot'
import { CartProvider } from '@/lib/cartContext'

export default function SiteLayout({ children }: { children: React.ReactNode }) {
  return (
    <CartProvider>
      <Navbar />
      <main className="pt-14">{children}</main>
      <Footer />
      <ColdLogicBot />
    </CartProvider>
  )
}
