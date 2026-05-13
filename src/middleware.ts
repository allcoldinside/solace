import { NextRequest, NextResponse } from 'next/server'

const AGE_GATED = ['/ccc', '/cartel']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const isAgeGated = AGE_GATED.some((p) => pathname.startsWith(p))

  if (isAgeGated) {
    const ageCookie = request.cookies.get('cold_age')
    if (ageCookie?.value !== 'verified') {
      const url = request.nextUrl.clone()
      url.pathname = '/age-gate'
      url.searchParams.set('dest', pathname)
      return NextResponse.redirect(url)
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/ccc/:path*', '/cartel/:path*'],
}
