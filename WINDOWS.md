# Windows quick reference

This project is designed to work on Linux, macOS, and Windows. The Makefile
assumes a Unix shell, so native Windows users have three options:

## Option 1 — Use WSL (recommended)

Install WSL2 (Ubuntu works great), then run everything inside WSL exactly as
the main README describes. The Linux binaries in `status-service/bin/` run
under WSL.

## Option 2 — Use Git Bash / MSYS2

Git Bash ships with `bash` and a recent Git install. `run.sh` works under
Git Bash. `make` does not ship with Git Bash by default — install it via
`choco install make` or `scoop install make`, or use Option 3 below.

## Option 3 — Native cmd.exe / PowerShell (no bash, no make)

Open three terminals and run these commands directly — no `make` needed.
To run one of the four neutral profiles, set `STATUS_PROFILE` to a value from
`1` through `4` before starting the status service. Observe the selected
profile's behavior; the profile number does not describe that behavior.

```cmd
:: Terminal 1 — status service with a neutral profile (choose 1, 2, 3, or 4)
set STATUS_PROFILE=1
status-service\run.bat

:: Terminal 1 alternative — disable chaos for clean debugging
set STATUS_PROFILE=
set STATUS_CHAOS_LATENCY_MS=0
set STATUS_CHAOS_ERROR_RATE=0
status-service\run.bat

:: Terminal 2 — your backend (adjust for your language)
cd backend
REM e.g. go run .   /   python -m uvicorn main:app   /   mvn spring-boot:run   /   npm start
<your-start-command>

:: Terminal 3 — frontend
cd frontend
npm ci
npm run dev
```

PowerShell equivalents for env vars:

```powershell
# Neutral profile (choose 1, 2, 3, or 4)
$env:STATUS_PROFILE = "1" # Choose 1, 2, 3, or 4.
.\status-service\run.bat

# Clean debugging alternative
Remove-Item Env:STATUS_PROFILE -ErrorAction SilentlyContinue
$env:STATUS_CHAOS_LATENCY_MS = "0"
$env:STATUS_CHAOS_ERROR_RATE = "0"
.\status-service\run.bat
```

## Binaries provided

`status-service/bin/` contains:

- `statussvc-linux-amd64`, `statussvc-linux-arm64` — for WSL / Linux
- `statussvc-darwin-amd64`, `statussvc-darwin-arm64` — for macOS
- `statussvc-windows-amd64.exe`, `statussvc-windows-arm64.exe` — for Windows

`run.sh` and `run.bat` auto-select the right one based on your platform.
