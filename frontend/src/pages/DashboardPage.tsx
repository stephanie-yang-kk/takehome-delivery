import { FormEvent, useEffect, useState } from 'react'
import {
  createService,
  getServiceStatus,
  listServices,
  type MonitoringService,
  type StatusResponse,
} from '../api/client'
import { getRole } from '../auth/session'
import { DataStateBadge, StatusBadge } from '../components/Badges'
import ErrorBanner from '../components/ErrorBanner'

const TARGETS = ['svcA', 'svcB', 'svcC', 'svcD', 'svcE']

interface ServiceRow {
  service: MonitoringService
  status: StatusResponse | null
  statusError: unknown
}

export default function DashboardPage() {
  const role = getRole()
  const [rows, setRows] = useState<ServiceRow[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<unknown>(null)
  const [creating, setCreating] = useState(false)
  const [name, setName] = useState('')
  const [target, setTarget] = useState(TARGETS[0])
  const [description, setDescription] = useState('')

  async function loadServices() {
    setLoading(true)
    setError(null)

    try {
      const response = await listServices()
      const nextRows = await Promise.all(
        response.items.map(async (service) => {
          try {
            const status = await getServiceStatus(service.id)
            return { service, status, statusError: null }
          } catch (statusError) {
            return { service, status: null, statusError }
          }
        }),
      )
      setRows(nextRows)
    } catch (err) {
      setError(err)
      setRows([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadServices()
  }, [])

  async function handleCreate(event: FormEvent) {
    event.preventDefault()
    setCreating(true)
    setError(null)

    try {
      await createService({
        name,
        target,
        description: description.trim() || undefined,
      })
      setName('')
      setDescription('')
      await loadServices()
    } catch (err) {
      setError(err)
    } finally {
      setCreating(false)
    }
  }

  return (
    <div className="stack-lg">
      <div className="page-header">
        <div>
          <h2>Service Dashboard</h2>
          <p className="muted">Monitoring targets and current status</p>
        </div>
        <button type="button" onClick={() => void loadServices()} disabled={loading}>
          Refresh
        </button>
      </div>

      {error ? <ErrorBanner error={error} /> : null}

      {role === 'admin' ? (
        <section className="panel">
          <h3>Add monitoring target</h3>
          <form className="grid-form" onSubmit={handleCreate}>
            <label className="field">
              <span>Name</span>
              <input value={name} onChange={(event) => setName(event.target.value)} required />
            </label>
            <label className="field">
              <span>Target</span>
              <select value={target} onChange={(event) => setTarget(event.target.value)}>
                {TARGETS.map((item) => (
                  <option key={item} value={item}>{item}</option>
                ))}
              </select>
            </label>
            <label className="field field-wide">
              <span>Description</span>
              <input
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                placeholder="Optional"
              />
            </label>
            <button type="submit" disabled={creating}>
              {creating ? 'Creating…' : 'Create target'}
            </button>
          </form>
        </section>
      ) : (
        <div className="banner banner-info">Signed in as viewer — create is disabled.</div>
      )}

      <section className="panel">
        <h3>Targets</h3>
        {loading ? <p className="muted">Loading…</p> : null}
        {!loading && rows.length === 0 ? <p className="muted">No monitoring targets yet.</p> : null}

        <div className="card-list">
          {rows.map(({ service, status, statusError }) => (
            <article key={service.id} className="card">
              <div className="card-header">
                <div>
                  <h4>{service.name}</h4>
                  <p className="muted">upstream: {service.target}</p>
                </div>
                <a href={`/services/${service.id}`}>Details</a>
              </div>

              {statusError ? <ErrorBanner error={statusError} /> : null}

              {status ? (
                <div className="inline-badges">
                  <StatusBadge status={status.status} />
                  <DataStateBadge dataState={status.data_state} />
                </div>
              ) : null}

              {service.description ? <p>{service.description}</p> : null}
            </article>
          ))}
        </div>
      </section>
    </div>
  )
}
