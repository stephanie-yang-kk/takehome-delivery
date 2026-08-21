# Start Here — The Clock Is Already Running

Read this file first.

The four-hour clock is already running when you open this file.
The assignment email receipt time is the official start time.
The deadline is four hours after the assignment email receipt time.

Setup, download, unzip, environment checks, smoke tests, and troubleshooting are included in the four-hour limit.

## Setup and smoke test

1. Download and unzip the package, then open a terminal in its root.
2. Check the tools needed for your chosen implementation:
   - Git.
   - The current stable Go release, current stable Python release, current
     stable Rust release, active-LTS Node.js release, or current LTS JDK for
     your backend.
   - Node.js 22.18 or newer and npm for the provided React frontend.
   - `curl` and an editor.
3. Initialize Git in the project root because the delivery package does not
   include a `.git` directory.
4. Run `make run-status-profile PROFILE=1`.
5. Verify `curl http://localhost:8090/api/v1/health` returns `{"status":"ok"}`.
6. Run `make install-frontend` and `make run-frontend`, then open
   <http://localhost:3000>.
7. Confirm that your chosen backend toolchain can start a basic HTTP listener
   on port `8080`.

See `WINDOWS.md` if you are using native Windows without `make`.

Your submission may use an embedded database. It must not require a separately
operated database, cloud account, paid service, or private package registry.
The provided status service is a prebuilt binary for common desktop platforms.

## Four-hour limit

- Stop at the stated deadline and submit the state you have.
- We suggest reserving the final 30 minutes for verification, handoff, and
  packaging. Avoid starting new work during that period.
- If download, setup, or a provided component fails, contact HR immediately
  with your operating system and the exact error.
- The clock does not pause automatically. Only written notice from HR changes
  the deadline.

## Assistance policy

- You may use AI tools of your choice.
- No human assistance is allowed.
- You remain responsible for understanding every submitted change.
- In `HANDOFF.md`, disclose the AI tools and models you used and the two
  required examples of output you accepted, corrected, or rejected
  in any combination, as described in `SUBMISSION.md`.

## Next steps

1. Read `README.md` for the scenario, outcomes, and scope.
2. Read `CONTRACT.md` for the stable technical requirements.
3. Read `SUBMISSION.md` for handoff requirements.
4. Read `WINDOWS.md` if it applies to your environment.
5. Read `backend/README.md` before creating the backend.
6. Create `OBSERVATIONS.md` during the first 25 minutes.
