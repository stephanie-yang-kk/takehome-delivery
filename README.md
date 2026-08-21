# Service Monitor Take-Home

Build a small service-monitoring application within four hours. The work should
show that users can sign in, manage monitoring targets with the right
permissions, and understand current and recent service health when upstream
data is imperfect.

Start with `START-HERE.md`, then read `CONTRACT.md` for the stable technical
requirements.

## Scenario

An operations team monitors five upstream targets through a read-only status
service. Admins register the targets the team cares about. Viewers inspect
their current state and availability over the last minute.

Upstream responses and availability vary while remaining within the contract.
Your application should communicate what it knows, what it does not know, and
when it used fallback data.

## User outcomes

- Users can authenticate, and admin/viewer permissions are enforced.
- Admins can configure monitoring targets while viewers can inspect them.
- Users can understand current status, recent availability, uncertainty, and
  fallback data.
- Ensure user-facing operations remain bounded under upstream delay or failure.
- Public requests can be correlated with upstream work and final outcomes
  without exposing secrets.
- A thin React interface makes the required workflows and failure states clear.

## Provided components

- Run `make run-status` to exercise ordinary operation with intermittent delay and failure.
  For initial debugging, `make run-status-clean` disables that injection.
- A read-only status-service binary with four neutral profiles. Start one with
  `make run-status-profile PROFILE=1`; valid values are `PROFILE=1` through `PROFILE=4`.
  The profiles expose representative valid upstream behavior, including behavior
  this document does not describe; explore before you assume.
  You should observe and document them; no behavior-to-profile mapping is
  provided. A profile run repeats identically across restarts, while
  `make run-status` does not.
- Stop the status service or point `STATUS_SERVICE_URL` to an unused local port
  to observe sustained unavailability.
- A provided React and TypeScript frontend skeleton for a thin React and TypeScript interface.
- An empty `backend/` workspace. Use any supported backend language and
  framework.
- Make targets for starting the provided components.

The status service runs on port `8090`, your backend runs on port `8080`, and
the frontend runs on port `3000`.

## Level 1 — Required core

Build a runnable vertical core with focused tests. Cover authentication and
admin/viewer authorization, monitoring-target configuration, current status
and recent availability, honest unknown or unavailable outcomes, bounded
failure behavior, request correlation, and the thin React experience.

The minimal compatibility fields, outcomes, upstream guarantees, and runtime
boundary are defined only in `CONTRACT.md`.
Keep tests integrated while building, not after coding. Leave usability and visual polish last.

## Level 2 — One extension direction

After the required core works, pick exactly one direction you have real
experience with. Do not implement it fully. Deliver only:

- The user or operator outcome, in at most 150 words: what someone can do
  afterwards that they cannot do now.
- One real seam in the code showing the direction is reachable — a hook,
  boundary, or configuration point — with one test proving it is wired in rather
  than sketched.
- What remains incomplete, and the first thing you would build next.
- One sentence on why you chose this direction, naming a situation in your own
  experience that motivated it.

Choose one coherent extension only after the required core works. Pick from
these broad directions:

- Mutation safety and auditability.
- Real-time operator experience.
- Abuse, configuration, or security controls.
- Durable history or background processing.
- Multi-instance correctness.
- Deployment and operability.
- Alternate integration boundary.

Depth of judgment matters here, not volume of code. A finished feature is not
better than a well-chosen seam.
An incomplete extension must not break the required core.
Document the extension contract and trade-offs in `HANDOFF.md`.

Do not modify the provided status service or replace the supplied frontend
skeleton.

## Handoff

- Timing, setup, and assistance rules: `START-HERE.md`
- Stable technical contract: `CONTRACT.md`
- Required submission files and packaging: `SUBMISSION.md`

The handoff includes `submission.json`, `OBSERVATIONS.md`, and `HANDOFF.md`.
We suggest using the final 30 minutes to verify commands and prepare the
handoff artifacts.
