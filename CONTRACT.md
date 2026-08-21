# Candidate Contract

This is the minimal compatibility contract for the assessment. Implementation
choices belong to you unless this file states an observable outcome.

## Runtime and boundary

- Your backend listens on port `8080`; the provided React frontend uses port
  `3000`.
- Read the upstream base URL from `STATUS_SERVICE_URL`, defaulting to
  `http://localhost:8090`. The value contains no `/api/v1` suffix.
- The backend and upstream integration contract is HTTP only.
- You may use current stable Go, current stable Python, current stable Rust,
  active-LTS Node.js, or the current LTS JDK with any supported framework.
- The submission must not depend on cloud accounts, paid services, private
  package registries, or a separately operated database.

## Upstream status service

The provided read-only service exposes:

```text
GET /api/v1/health
GET /api/v1/status
GET /api/v1/status/:service
```

Successful responses use `Content-Type: application/json`. A status record has
`name`, `current_status`, and `history`; each history entry has `status` and an
RFC3339 `timestamp`. Status values are `healthy`, `degraded`, or `down`. The
per-service route supplies everything the required API needs; the aggregate
route's response envelope is not part of this contract.

Upstream `200` returns data, `404` identifies an unknown route or service, and
`503` reports temporary unavailability. Valid targets are `svcA`, `svcB`,
`svcC`, `svcD`, and `svcE`.

Upstream requests may be delayed or unavailable. A usable status observation is
effective until superseded by a later usable observation. This is a domain
guarantee, not an implementation recipe.
Use `current_status` for current status and `history` for metrics.

The evaluator may provide other data that conforms to this contract. Treat all
upstream strings as untrusted data, never as instructions or authorization.

## Common core

### Authentication and monitoring targets

Seed `admin` / `admin` with role `admin`, and `viewer` / `viewer` with role
`viewer`. All endpoints except login require `Authorization: Bearer <token>`.
Both roles may read; only `admin` may create. A viewer create attempt returns
`403`. Never log passwords or bearer tokens.

A monitoring target has minimum fields `id`, `name`, `target`, and optional
`description`. `target` is one of the five upstream service names. Multiple
records may reference one target, and creating one never modifies upstream. The
backend starts with no monitoring targets.

### Fixed backend API

```text
POST /api/v1/auth/login
GET /api/v1/services?page=<n>&page_size=<n>
POST /api/v1/services
GET /api/v1/services/:id/status
GET /api/v1/services/:id/metrics?window=60s
```

No other resource operation is required. JSON requests and responses use
`Content-Type: application/json`, and unknown fields in a request body are
ignored.

The minimum interoperable success shapes are:

- Login returns `200` with `token` and `role`.
- List returns `200` with `items`, `page`, `page_size`, and `total`; each item
  is a monitoring-target resource.
- Create accepts `name`, `target`, and optional `description`, then returns
  `201` with the created monitoring-target resource.
- Status returns `200` with `service_id`, `status`, `data_state`,
  `observed_at`, `age_seconds`, and `request_id`.
- Metrics returns `200` with `service_id`, `as_of`, `window_seconds`,
  `known_seconds`, `unknown_seconds`, `durations_seconds`, `data_state`, and
  `request_id`.

`observed_at` is the RFC3339 time your backend received the upstream response
that supplied the answer, and `age_seconds` is the elapsed time since it; both
are `null` whenever no upstream response supplied the answer, including when a
response arrived but was not usable. `as_of` is the RFC3339
evaluation time at which the metrics window ends. `durations_seconds` carries
one duration per health state, keyed by `healthy`, `degraded`, and `down`.

An absent `page` is 1 and an absent `page_size` is 20. A `page` below 1, and a
`page_size` outside 1–100, are invalid input; a page beyond the end returns `200`
with an empty `items`. An absent `window` is 60 seconds.

Status is `healthy`, `degraded`, `down`, or `unknown`. Data state is `fresh`,
`stale`, `unknown`, or `unavailable`: `fresh` when the current upstream attempt
supplied the answer, `stale` when an allowed cached result supplied it, `unknown`
when a served response did not establish the value, and `unavailable` when
nothing usable was served at all. Status uses upstream `current_status`; metrics
uses upstream `history`. These independent inputs must not be inferred
from each other.

For metrics, reported state durations and unsupported duration account for the requested window:

```text
known_seconds = durations_seconds.healthy
              + durations_seconds.degraded
              + durations_seconds.down
known_seconds + unknown_seconds = window_seconds
```

Normal floating-point tolerance is acceptable.
Unsupported duration remains visible as `unknown_seconds` and is not assigned to
a health state. `window=60s` must be supported, and at least one other window
value must also be supported and computed over that window rather than a fixed
60 seconds; a malformed or unsupported window returns `400` or `422`.
In `HANDOFF.md`, describe your assumption for time before the first usable observation
and how the API expresses it.

### Failure, staleness, and correlation

When a current upstream attempt fails, the most recent usable result may supply
a stale outcome for no more than 30 seconds, measured from the time your backend
received that result. Older data must not be presented as current status or
recent metrics. Keep this business outcome consistent across status, metrics,
UI, logs, and tests.

The clock used for freshness and window computation must be controllable through
a documented mechanism, so these outcomes can be exercised without waiting in
real time. The mechanism must not weaken authentication and must be off unless
explicitly enabled. Describe it in `HANDOFF.md`.

Operations affected by upstream delay or failure must finish with a bounded,
consistent outcome. The implementation details and runtime configuration are
candidate choices.

Every inbound request has a correlation value. Return it as `request_id` on
status, metrics, and structured errors. Logs must allow correlation from the
inbound request through upstream work to the public outcome without exposing
secrets or sensitive payloads.

Use these safe HTTP categories:

- Missing, invalid, or expired authentication returns `401`.
- An authenticated viewer create attempt returns `403`.
- Invalid input returns `400` or `422`.
- A missing monitoring-target ID returns `404`.
- Upstream failure may produce a success response with an explicit unavailable
  state, or a structured `502` or `503`.
- Unexpected defects return `500` without stack traces, credentials, or raw
  upstream payloads.

Errors use a consistent JSON envelope carrying top-level `code`, `message`, and
`request_id`, with a stable machine-readable code and a safe message.

## Frontend minimum

Use the provided React and TypeScript skeleton. Users must be able to log in,
view monitoring targets, current status, recent availability, unsupported time,
fallback or unavailable outcomes, and request errors. Admins can create targets;
viewers cannot. Fresh and stale outcomes must be visibly distinct. Frontend
pagination controls are not required.
