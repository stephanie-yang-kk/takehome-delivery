# Submission

Reserve the final 30 minutes of the four-hour limit for this handoff. The
scenario and scope are in `README.md`; stable technical requirements are in
`CONTRACT.md`.

## Required files

### `submission.json`

Create this file at the repository root:

```json
{
  "setup_command": "command or empty string",
  "backend_start_command": "command run from repository root",
  "backend_test_command": "command run from repository root",
  "frontend_start_command": "command run from repository root",
  "frontend_test_command": "command or empty string"
}
```

Every command must be non-interactive. Use an empty string only where the shape
explicitly permits it.

### Regressions your tests must catch

Running `backend_test_command` must fail if any of these is introduced:

- the stale limit becomes 300 seconds instead of 30;
- a viewer is allowed to create a monitoring target;
- metrics ignore the requested window and always report 60 seconds.

Name the covering test for each in `HANDOFF.md`. A non-empty
`frontend_test_command` must run at least one test you wrote, not only the tests
shipped with the skeleton.

### `OBSERVATIONS.md`

Maximum 200 words. Write this during the first 25 minutes and do not revise it
after implementation begins. Answer two questions:

- What did you see when you ran the profiles that you would not have guessed
  from the documents?
- What are you choosing not to build, and why?

This file provides context for discussing how early assumptions compared with
the final implementation.

### `HANDOFF.md`

Maximum 1,200 words. Include:

- Run and test commands.
- Implemented and intentionally omitted scope.
- The extension direction you chose, or an explicit statement that you chose
  none.
- Its outcome, the seam you built, what remains incomplete, and why you chose
  it.
- Public profile observations and how they influenced decisions.
- Evidence that the 30-second stale limit and bounded failure outcomes hold.
- The documented mechanism for controlling freshness and window time, and the
  test that covers each regression listed above.
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
- If you used AI, two concrete examples of output you accepted, corrected, or rejected in any combination, with a short reason per example.

Full prompts and chat histories are not required.

## Git repository

Keep the `.git` directory in the submission. Commit history is review context
only; use it to make the work easy to follow.

Do not commit credentials, bearer tokens, generated dependencies, build output,
database files, or the provided status-service binaries.

## Package and send

1. Run the test commands recorded in `submission.json`.
2. Check that all five command fields are correct and non-interactive.
3. Remove generated files such as `node_modules`, build output, local databases,
   logs, and environment files.
4. Zip the repository, including `.git`, while excluding
   `status-service/bin/`.
5. Send the archive using the instructions from your hiring coordinator.

Excluding `status-service/bin/` keeps the archive small. Before startup, the
evaluation environment restores the original, immutable provided binaries.
Their absence from your archive is not a candidate startup failure.

Example:

```bash
zip -r takehome-submission.zip . \
  -x ".DS_Store" "status-service/bin/*" "frontend/node_modules/*" "frontend/dist/*"
```

## Final checklist

- [ ] `submission.json` has every required field and working commands.
- [ ] `OBSERVATIONS.md` is no more than 500 words.
- [ ] `HANDOFF.md` is no more than 1,200 words and contains every required
      section.
- [ ] The chosen extension direction, its seam, and remaining work are
      documented.
- [ ] Stale fallback, initial-gap, and bounded-failure evidence is included.
- [ ] `backend_test_command` fails under each listed regression.
- [ ] The freshness and window clock mechanism is documented.
- [ ] The backend reads the upstream base URL from `STATUS_SERVICE_URL`.
- [ ] Backend and frontend tests have been run.
- [ ] `.git` is present.
- [ ] Generated files, secrets, and provided binaries are excluded.
