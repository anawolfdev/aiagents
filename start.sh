#!/usr/bin/env bash
# start.sh <FEATURE-ID> [--ticket-id <UUID>] — sync + claim remoto + start local
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "$#" -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
  printf '%s\n' 'Uso: start.sh <FEATURE-ID> [--ticket-id <UUID>]' 'Requiere GEAS_ACTOR_ID; UUID explícito o mapping previo con harness link.'
  exit 0
fi
FEATURE="$1"; shift
cd "$ROOT"
exec uv run python -m agents --json run harness start --id "$FEATURE" "$@"
