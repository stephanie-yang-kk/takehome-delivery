import { useEffect, useState } from 'react'
import { getServiceMetrics, getServiceStatus, type MetricsResponse, type StatusResponse } from '../api/client'
import { DataStateBadge, StatusBadge } from '../components/Badges'
import ErrorBanner from '../components/ErrorBanner'

function formatSeconds(value: number | null | undefined): string {
  if (value === null || value === undefined) {
    return '—'
  }
  return `${value.toFixed(1)}s`
}

function formatTimestamp(value: string | null | undefined): string {
  if (!value) {
    return '—'
  }
  return new Date(value).toLocaleString()
}

interface ServiceDetailPageProps {
  id: string
}

const WINDOW_OPTIONS = ['60s', '300s'] as const

export default function ServiceDetailPage({ id }: ServiceDetailPageProps) {
  const [status, setStatus] = useState<StatusResponse | null>(null)
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null)
  const [window, setWindow] = useState<(typeof WINDOW_OPTIONS)[number]>('60s')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<unknown>(null)

  async function loadDetail(selectedWindow: (typeof WINDOW_OPTIONS)[number]) {
    setLoading(true)
    setError(null)

    try {
      const [nextStatus, nextMetrics] = await Promise.all([
        getServiceStatus(id),
        getServiceMetrics(id, selectedWindow),
      ])
      setStatus(nextStatus)
      setMetrics(nextMetrics)
    } catch (err) {
      setError(err)
      setStatus(null)
      setMetrics(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadDetail(window)
  }, [id, window])

  return (
    <div className="stack-lg">
      <div className="page-header">
        <div>
          <h2>Service detail</h2>
          <p className="muted">ID: {id}</p>
        </div>
        <a href="/dashboard">Back to dashboard</a>
      </div>

      {error ? <ErrorBanner error={error} /> : null}
      {loading ? <p className="muted">Loading…</p> : null}

      {status ? (
        <section className="panel">
          <h3>Current status</h3>
          <div className="inline-badges">
            <StatusBadge status={status.status} />
            <DataStateBadge dataState={status.data_state} />
          </div>
          <dl className="detail-grid">
            <div>
              <dt>Observed at</dt>
              <dd>{formatTimestamp(status.observed_at)}</dd>
            </div>
            <div>
              <dt>Age</dt>
              <dd>{formatSeconds(status.age_seconds)}</dd>
            </div>
            <div>
              <dt>Request ID</dt>
              <dd>{status.request_id}</dd>
            </div>
          </dl>
          {status.data_state === 'stale' ? (
            <p className="banner banner-warning">
              Showing cached data because the latest upstream check did not succeed.
            </p>
          ) : null}
          {status.data_state === 'unavailable' ? (
            <p className="banner banner-error">
              No usable status is available right now.
            </p>
          ) : null}
        </section>
      ) : null}

      <section className="panel">
        <div className="page-header">
          <h3>Recent availability</h3>
          <label className="field inline-field">
            <span>Window</span>
            <select value={window} onChange={(event) => setWindow(event.target.value as typeof window)}>
              {WINDOW_OPTIONS.map((option) => (
                <option key={option} value={option}>{option}</option>
              ))}
            </select>
          </label>
        </div>

        {metrics ? (
          <>
            <div className="inline-badges">
              <DataStateBadge dataState={metrics.data_state} />
            </div>
            <dl className="detail-grid">
              <div>
                <dt>As of</dt>
                <dd>{formatTimestamp(metrics.as_of)}</dd>
              </div>
              <div>
                <dt>Window</dt>
                <dd>{metrics.window_seconds}s</dd>
              </div>
              <div>
                <dt>Unknown time</dt>
                <dd>{formatSeconds(metrics.unknown_seconds)}</dd>
              </div>
              <div>
                <dt>Request ID</dt>
                <dd>{metrics.request_id}</dd>
              </div>
            </dl>

            <table className="metrics-table">
              <thead>
                <tr>
                  <th>State</th>
                  <th>Duration</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><StatusBadge status="healthy" /></td>
                  <td>{formatSeconds(metrics.durations_seconds.healthy)}</td>
                </tr>
                <tr>
                  <td><StatusBadge status="degraded" /></td>
                  <td>{formatSeconds(metrics.durations_seconds.degraded)}</td>
                </tr>
                <tr>
                  <td><StatusBadge status="down" /></td>
                  <td>{formatSeconds(metrics.durations_seconds.down)}</td>
                </tr>
                <tr className="unknown-row">
                  <td>unsupported / unknown</td>
                  <td>{formatSeconds(metrics.unknown_seconds)}</td>
                </tr>
              </tbody>
            </table>
          </>
        ) : null}
      </section>
    </div>
  )
}
