# Candidates on Windows without `make` installed: use WSL / Git Bash, or run
# the commands in each target directly. See WINDOWS.md for cmd-line equivalents.
#
# There is no `run-backend` target — backend/ is language-agnostic. Start your
# backend however your stack requires.
.PHONY: run-status run-status-profile run-status-clean run-frontend install-frontend help

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

run-status: ## Start the status service (HTTP :8090) — chaos ON by default
	@test -x ./status-service/run.sh || { echo "ERROR: missing executable status-service/run.sh" >&2; exit 2; }
	./status-service/run.sh

run-status-profile: ## Start the status service with neutral PROFILE=1..4
	@case "$(PROFILE)" in 1|2|3|4) ;; *) echo "ERROR: PROFILE must be exactly one of 1, 2, 3, or 4" >&2; exit 2 ;; esac
	@test -x ./status-service/run.sh || { echo "ERROR: missing executable status-service/run.sh" >&2; exit 2; }
	STATUS_PROFILE=$(PROFILE) ./status-service/run.sh

run-status-clean: ## Start the status service with NO chaos (for initial debugging only)
	@test -x ./status-service/run.sh || { echo "ERROR: missing executable status-service/run.sh" >&2; exit 2; }
	env -u STATUS_PROFILE STATUS_CHAOS_LATENCY_MS=0 STATUS_CHAOS_ERROR_RATE=0 ./status-service/run.sh

install-frontend: ## Install exact locked frontend dependencies
	cd frontend && npm ci

run-frontend: ## Start the frontend dev server (HTTP :3000)
	cd frontend && npm run dev
