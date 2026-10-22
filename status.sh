#!/usr/bin/env bash
# status.sh — puerta sincronizada; --json / --quick como init.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$ROOT/init.sh" "$@"
