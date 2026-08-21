import type { ReactNode } from 'react'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div>
      <header style={{
        padding: '0.75rem 1.5rem',
        borderBottom: '1px solid #e0e0e0',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <a href="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>
          <h1 style={{ fontSize: '1.25rem', fontWeight: 600 }}>Service Monitor</h1>
        </a>
        {/* TODO */}
      </header>
      <main style={{ padding: '1.5rem' }}>
        {children}
      </main>
    </div>
  )
}
