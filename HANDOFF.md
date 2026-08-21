
- Run and test commands.
  - `submission.json`
- Implemented and intentionally omitted scope.
  - Implemented:
    - login and auth
    - monitoring crud
    - status stale
    - frontend
  - Omitted
    - token expiry policy
- The extension direction you chose, or an explicit statement that you chose
  none.
  - Audit
- Its outcome, the seam you built, what remains incomplete, and why you chose
  it.
  - writing `audit_logs` table after admin creating a target
  - incomplete: API to fetch audit_logs table
  - why? having audit 
- Public profile observations and how they influenced decisions.
- Evidence that the 30-second stale limit and bounded failure outcomes hold.
  - `get_stale`
- The documented mechanism for controlling freshness and window time, and the
  test that covers each regression listed above.
  - under tests dir
- Your initial-gap assumption before the first usable observation, how the API
  expresses it, and evidence that unsupported duration remains visible.
- Cross-layer consistency across API responses, UI states, logs, and tests.
- One technical decision record: constraints, considered alternatives,
  decision, downside, and reversal trigger.
- Two places where running something changed your mind, including the specific
  observation that changed it and what you did about it.
- Known defects and risks.
- The one thing in your own implementation you expect to fail first in
  production, why, and how you would find out.
- AI tools and models used, or an explicit statement that none were used.
  - gpt-5.6
- If you used AI, two concrete examples of output you accepted, corrected, or rejected in any combination, with a short reason per example.
  - Accepted: frontend codes, because I'm not very familiar with frontend languages
  - Rejected: initial project structure, decide to refactor into api-service-dao 3-layer structure for better human understanding

