import { FormEvent, useState } from 'react'
import { login } from '../api/client'
import { setSession } from '../auth/session'
import ErrorBanner from '../components/ErrorBanner'

export default function LoginPage() {
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('admin')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<unknown>(null)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const result = await login(username, password)
      setSession(result.token, result.role)
      window.location.href = '/dashboard'
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="panel narrow">
      <h2>Login</h2>
      <p className="muted">Seed users: admin/admin or viewer/viewer</p>

      {error ? <ErrorBanner error={error} /> : null}

      <form className="stack" onSubmit={handleSubmit}>
        <label className="field">
          <span>Username</span>
          <input
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            autoComplete="username"
            required
          />
        </label>

        <label className="field">
          <span>Password</span>
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
            required
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? 'Signing in…' : 'Sign in'}
        </button>
      </form>
    </div>
  )
}
