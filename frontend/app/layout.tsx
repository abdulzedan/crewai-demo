// frontend/app/layout.tsx
import './globals.css'
import type { Metadata } from 'next'
import React from 'react'

export const metadata: Metadata = {
  title: 'Collaborative Writing',
  description: 'Multi-agent writing with Next.js + Tailwind + shadcn/ui',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="h-full w-full bg-gray-100 text-gray-900">
        {children}
      </body>
    </html>
  )
}
