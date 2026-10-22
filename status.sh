#!/usr/bin/env bash
# status.sh — ¿se puede trabajar en este repositorio? (spec §25)
#   ./status.sh          → READY TO WORK / NOT READY
#   ./status.sh --json   → salida estructurada para agentes
set -uo pipefail
if command -v geas >/dev/null 2>&1; then
  geas work status "${PWD}" "$@"
else
  exec uv run --project "$(git rev-parse --show-toplevel)/.." python -m geas.work status "${PWD}" "$@"
fi
