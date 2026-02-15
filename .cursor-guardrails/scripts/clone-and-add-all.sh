#!/usr/bin/env bash
# Clone all jobk84092 repos (from scripts/repos.txt) into a directory,
# then add cursor-guardrails to each. Fully automatic for "all repos".
#
# Usage:
#   scripts/clone-and-add-all.sh [target_dir] [github_user]
#
# Default target_dir: $HOME/github/jobk84092 (or $HOME/repos if you prefer)
# Default github_user: jobk84092
#
# Run from cursor-guardrails repo root.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUARDRAILS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPOS_FILE="$SCRIPT_DIR/repos.txt"
TARGET_DIR="${1:-$HOME/github/jobk84092}"
GITHUB_USER="${2:-jobk84092}"

mkdir -p "$TARGET_DIR"
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

echo "Target directory: $TARGET_DIR"
echo "GitHub user: $GITHUB_USER"
echo ""

# Read repo names (skip comments and empty lines)
REPOS=()
while IFS= read -r line || [[ -n "$line" ]]; do
  line="${line%%#*}"
  line="$(echo "$line" | tr -d ' \r\n')"
  [[ -z "$line" ]] && continue
  REPOS+=("$line")
done < "$REPOS_FILE"

# Skip cursor-guardrails in the list (we're already in it)
for i in "${!REPOS[@]}"; do
  [[ "${REPOS[$i]}" == "cursor-guardrails" ]] && unset 'REPOS[i]'
done

echo "Repos from repos.txt: ${REPOS[*]}"
echo ""

for name in "${REPOS[@]}"; do
  dir="$TARGET_DIR/$name"
  if [[ -d "$dir/.git" ]]; then
    echo "Already cloned: $name"
  else
    echo "Cloning $name into $dir"
    git clone "https://github.com/${GITHUB_USER}/${name}.git" "$dir"
  fi
done

echo ""
echo "Adding guardrails to all repos in $TARGET_DIR ..."
bash "$SCRIPT_DIR/add-to-all-repos.sh" "$TARGET_DIR"

echo ""
echo "All set. Repos are in $TARGET_DIR with guardrails installed."
