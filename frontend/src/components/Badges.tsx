interface StatusBadgeProps {
  status: string
}

interface DataStateBadgeProps {
  dataState: string
}

const DATA_STATE_LABELS: Record<string, string> = {
  fresh: 'Fresh',
  stale: 'Stale (cached)',
  unknown: 'Unknown',
  unavailable: 'Unavailable',
}

export function StatusBadge({ status }: StatusBadgeProps) {
  return <span className={`badge badge-status badge-status-${status}`}>{status}</span>
}

export function DataStateBadge({ dataState }: DataStateBadgeProps) {
  const label = DATA_STATE_LABELS[dataState] ?? dataState
  return <span className={`badge badge-data-state badge-data-state-${dataState}`}>{label}</span>
}
