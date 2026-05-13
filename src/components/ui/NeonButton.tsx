'use client'

import Link from 'next/link'
import { ReactNode } from 'react'

interface NeonButtonProps {
  children: ReactNode
  href?: string
  onClick?: () => void
  variant?: 'outline' | 'solid' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  className?: string
  type?: 'button' | 'submit'
  disabled?: boolean
}

export default function NeonButton({
  children,
  href,
  onClick,
  variant = 'outline',
  size = 'md',
  className = '',
  type = 'button',
  disabled = false,
}: NeonButtonProps) {
  const base =
    'font-mono tracking-widest uppercase transition-all duration-200 inline-block cursor-pointer'

  const variants = {
    outline:
      'border border-cold-green text-cold-green hover:bg-cold-green hover:text-cold-black',
    solid: 'bg-cold-green text-cold-black font-bold hover:opacity-90',
    ghost: 'text-cold-smoke hover:text-cold-green border-b border-transparent hover:border-cold-green',
  }

  const sizes = {
    sm: 'px-4 py-2 text-xs',
    md: 'px-6 py-3 text-sm',
    lg: 'px-8 py-4 text-base',
  }

  const cls = `${base} ${variants[variant]} ${sizes[size]} ${disabled ? 'opacity-40 cursor-not-allowed' : ''} ${className}`

  if (href) {
    return (
      <Link href={href} className={cls}>
        {children}
      </Link>
    )
  }

  return (
    <button type={type} onClick={onClick} className={cls} disabled={disabled}>
      {children}
    </button>
  )
}
