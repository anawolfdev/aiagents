#!/usr/bin/env bash
# sync.sh — sincroniza el repo con Geas y con Git (spec §24)
set -uo pipefail
if command -v geas >/dev/null 2>&1; then
  geas work sync "${PWD}"
else
  exec uv run --project "$(git rev-parse --show-toplevel)/.." python -m geas.work sync "${PWD}"
fi
