const TOKEN_KEY = 'sm_token'
const ROLE_KEY = 'sm_role'

export type UserRole = 'admin' | 'viewer'

export function getToken(): string | null {
  return sessionStorage.getItem(TOKEN_KEY)
}

export function getRole(): UserRole | null {
  const role = sessionStorage.getItem(ROLE_KEY)
  if (role === 'admin' || role === 'viewer') {
    return role
  }
  return null
}

export function setSession(token: string, role: UserRole): void {
  sessionStorage.setItem(TOKEN_KEY, token)
  sessionStorage.setItem(ROLE_KEY, role)
}

export function clearSession(): void {
  sessionStorage.removeItem(TOKEN_KEY)
  sessionStorage.removeItem(ROLE_KEY)
}

export function isLoggedIn(): boolean {
  return getToken() !== null && getRole() !== null
}
