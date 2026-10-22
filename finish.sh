#!/usr/bin/env bash
# finish.sh <FEATURE-ID> --evidence <salida> [--yes] — puerta + push + cierre GEAS
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "$#" -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
  printf '%s\n' 'Uso: finish.sh <FEATURE-ID> --evidence "<salida real>" [--yes]' 'Entregables commiteados y ticket asociado. --yes autoriza push al upstream, sin commit automático.'
  exit 0
fi
FEATURE="$1"; shift
cd "$ROOT"
exec uv run python -m agents --json run harness finish --id "$FEATURE" "$@"
