export function parseErrorBody(body: unknown): { code: string; message: string; request_id?: string } {
  if (typeof body === 'object' && body !== null) {
    const record = body as Record<string, unknown>
    return {
      code: typeof record.code === 'string' ? record.code : 'unknown_error',
      message: typeof record.message === 'string' ? record.message : 'Request failed',
      request_id: typeof record.request_id === 'string' ? record.request_id : undefined,
    }
  }
  return { code: 'unknown_error', message: 'Request failed' }
}
