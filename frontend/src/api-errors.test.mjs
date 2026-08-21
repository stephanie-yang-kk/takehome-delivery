import assert from 'node:assert/strict'
import test from 'node:test'
import { parseErrorBody } from './api/parseError.ts'

test('parseErrorBody extracts structured API errors', () => {
  assert.deepEqual(parseErrorBody({
    code: 'forbidden',
    message: 'Admin role required',
    request_id: 'req-123',
  }), {
    code: 'forbidden',
    message: 'Admin role required',
    request_id: 'req-123',
  })
})

test('parseErrorBody falls back for invalid payloads', () => {
  assert.deepEqual(parseErrorBody(null), {
    code: 'unknown_error',
    message: 'Request failed',
  })
})
