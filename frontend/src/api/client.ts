import { getToken } from '../auth/session'
import { parseErrorBody } from './parseError'

export class ApiError extends Error {
  status: number
  code: string
  requestId?: string

  constructor(status: number, code: string, message: string, requestId?: string) {
    super(message)
    this.status = status
    this.code = code
    this.requestId = requestId
  }
}

export interface MonitoringService {
  id: string
  name: string
  target: string
  description?: string | null
}

export interface ServiceListResponse {
  items: MonitoringService[]
  page: number
  page_size: number
  total: number
}

export interface StatusResponse {
  service_id: string
  status: 'healthy' | 'degraded' | 'down' | 'unknown'
  data_state: 'fresh' | 'stale' | 'unknown' | 'unavailable'
  observed_at: string | null
  age_seconds: number | null
  request_id: string
}

export interface MetricsResponse {
  service_id: string
  as_of: string
  window_seconds: number
  known_seconds: number
  unknown_seconds: number
  durations_seconds: {
    healthy: number
    degraded: number
    down: number
  }
  data_state: 'fresh' | 'stale' | 'unknown' | 'unavailable'
  request_id: string
}

async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  headers.set('Content-Type', 'application/json')

  const token = getToken()
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(path, { ...init, headers })
  const text = await response.text()
  const body = text ? JSON.parse(text) : null

  if (!response.ok) {
    const error = parseErrorBody(body)
    throw new ApiError(response.status, error.code, error.message, error.request_id)
  }

  return body as T
}

export async function login(username: string, password: string): Promise<{ token: string; role: 'admin' | 'viewer' }> {
  return apiFetch('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

export async function listServices(): Promise<ServiceListResponse> {
  return apiFetch('/api/v1/services')
}

export async function createService(input: {
  name: string
  target: string
  description?: string
}): Promise<MonitoringService> {
  return apiFetch('/api/v1/services', {
    method: 'POST',
    body: JSON.stringify(input),
  })
}

export async function getServiceStatus(serviceId: string): Promise<StatusResponse> {
  return apiFetch(`/api/v1/services/${serviceId}/status`)
}

export async function getServiceMetrics(serviceId: string, window = '60s'): Promise<MetricsResponse> {
  return apiFetch(`/api/v1/services/${serviceId}/metrics?window=${encodeURIComponent(window)}`)
}
