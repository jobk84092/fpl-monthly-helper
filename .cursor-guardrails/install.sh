#!/usr/bin/env bash
# Install shared Cursor guardrails into the current project's .cursor/rules/
# Run from project root. Use either:
#   .cursor-guardrails/install.sh
#   install.sh --source /path/to/cursor-guardrails

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUARDRAILS_ROOT="$(cd "$SCRIPT_DIR" && pwd)"
PROJECT_ROOT=""

if [[ "$1" == "--source" && -n "$2" ]]; then
  GUARDRAILS_ROOT="$(cd "$2" && pwd)"
  PROJECT_ROOT="$(pwd)"
else
  # Script lives at <project>/.cursor-guardrails/install.sh → project root is parent of script dir
  PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

RULES_SRC="$GUARDRAILS_ROOT/rules"
RULES_DST="$PROJECT_ROOT/.cursor/rules"

if [[ ! -d "$RULES_SRC" ]]; then
  echo "Error: rules dir not found at $RULES_SRC" >&2
  exit 1
fi

mkdir -p "$RULES_DST"

for f in "$RULES_SRC"/*.mdc; do
  [[ -f "$f" ]] || continue
  name="$(basename "$f")"
  cp "$f" "$RULES_DST/$name"
  echo "Installed: .cursor/rules/$name"
done

echo "Done. Cursor will load rules from $RULES_DST"
