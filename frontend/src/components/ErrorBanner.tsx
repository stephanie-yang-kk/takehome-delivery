import { ApiError } from '../api/client'

interface ErrorBannerProps {
  error: unknown
}

export default function ErrorBanner({ error }: ErrorBannerProps) {
  if (!(error instanceof ApiError)) {
    return (
      <div className="banner banner-error">
        Something went wrong. Please try again.
      </div>
    )
  }

  return (
    <div className="banner banner-error">
      <strong>{error.message}</strong>
      <div className="meta">
        code: {error.code}
        {error.requestId ? ` · request_id: ${error.requestId}` : null}
      </div>
    </div>
  )
}
