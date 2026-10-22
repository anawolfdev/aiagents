#!/usr/bin/env bash
# start.sh <ticket_id> — empieza a trabajar en un ticket (spec §24)
set -uo pipefail
if [ -z "$1" ]; then
  echo "Uso: ./start.sh <ticket_id>"
  exit 1
fi
if command -v geas >/dev/null 2>&1; then
  geas work start "$1" "${PWD}"
else
  exec uv run --project "$(git rev-parse --show-toplevel)/.." python -m geas.work start "$1" "${PWD}"
fi
