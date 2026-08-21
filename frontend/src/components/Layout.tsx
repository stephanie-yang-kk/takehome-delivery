import type { ReactNode } from 'react'
import { clearSession, getRole } from '../auth/session'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const role = getRole()

  function handleLogout() {
    clearSession()
    window.location.href = '/login'
  }

  return (
    <div>
      <header className="app-header">
        <a href="/dashboard" className="brand-link">
          <h1>Service Monitor</h1>
        </a>
        <div className="header-actions">
          {role ? <span className="role-pill">{role}</span> : null}
          <button type="button" onClick={handleLogout}>Log out</button>
        </div>
      </header>
      <main className="app-main">
        {children}
      </main>
    </div>
  )
}
