import assert from 'node:assert/strict'
import test from 'node:test'
import { parseRoute } from './routes.ts'

test('parses the login route', () => {
  assert.deepEqual(parseRoute('/login'), { page: 'login' })
})

test('parses the dashboard route', () => {
  assert.deepEqual(parseRoute('/dashboard'), { page: 'dashboard' })
})

test('extracts a service id', () => {
  assert.deepEqual(parseRoute('/services/service-42'), {
    page: 'service',
    id: 'service-42',
  })
})

test('marks unknown and incomplete paths as unknown', () => {
  assert.deepEqual(parseRoute('/'), { page: 'unknown' })
  assert.deepEqual(parseRoute('/services/'), { page: 'unknown' })
  assert.deepEqual(parseRoute('/not-a-page'), { page: 'unknown' })
})
