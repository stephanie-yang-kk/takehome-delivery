export type Route =
  | { page: 'login' }
  | { page: 'dashboard' }
  | { page: 'service'; id: string }
  | { page: 'unknown' }

export function parseRoute(pathname: string): Route {
  if (pathname === '/login') {
    return { page: 'login' }
  }

  if (pathname === '/dashboard') {
    return { page: 'dashboard' }
  }

  const serviceMatch = pathname.match(/^\/services\/([^/]+)$/)
  if (serviceMatch) {
    return { page: 'service', id: serviceMatch[1] }
  }

  return { page: 'unknown' }
}
