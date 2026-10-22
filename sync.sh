#!/usr/bin/env bash
# sync.sh — sincroniza el repo con Geas y con Git (spec §24)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  printf '%s\n' 'Uso: sync.sh — Git fetch/pull ff-only local + API GEAS con GEAS_ACTOR_ID; nunca push/commit.'
  exit 0
fi
cd "$ROOT"
exec uv run python -m agents --json run harness sync "$@"
