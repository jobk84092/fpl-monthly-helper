#!/usr/bin/env bash
# Add cursor-guardrails to all repos automatically.
#
# Usage:
#   1. From cursor-guardrails repo root:
#      scripts/add-to-all-repos.sh <parent_dir>
#      → Finds every direct subdir of <parent_dir> that is a git repo (except
#        cursor-guardrails) and adds the submodule + runs install.
#   2. With a list of repo paths:
#      scripts/add-to-all-repos.sh /path/to/repo1 /path/to/repo2 ...
#
# Requires: run from cursor-guardrails repo root, or set GUARDRAILS_REPO_ROOT.

set -e

GUARDRAILS_REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GUARDRAILS_URL="${CURSOR_GUARDRAILS_URL:-https://github.com/jobk84092/cursor-guardrails.git}"
REPOS=()

usage() {
  echo "Usage: add-to-all-repos.sh [--local] <parent_dir>"
  echo "   or: add-to-all-repos.sh [--local] /path/to/repo1 /path/to/repo2 ..."
  echo ""
  echo "Adds .cursor-guardrails (submodule or --local copy) and runs install in each repo."
  echo "  --local  copy from this repo instead of git submodule (use before pushing to GitHub)"
  echo "  CURSOR_GUARDRAILS_URL  override the guardrails repo URL for submodule."
  exit 0
}

USE_LOCAL=false
ARGS=()
for a in "$@"; do
  if [[ "$a" == "--local" ]]; then
    USE_LOCAL=true
  else
    ARGS+=("$a")
  fi
done
set -- "${ARGS[@]}"

# Collect repo directories (expand ~ in paths)
expand() { echo "$1"; }
if [[ -n "$HOME" ]]; then
  expand() { echo "${1/#\~/$HOME}"; }
fi

if [[ $# -eq 0 ]]; then
  echo "Error: no repo path(s) given." >&2
  usage
fi

PARENT="$(expand "$1")"
if [[ $# -eq 1 && -d "$PARENT" ]]; then
  for d in "$PARENT"/*/; do
    [[ -d "$d/.git" ]] || continue
    name="$(basename "$d")"
    if [[ "$name" == "cursor-guardrails" ]]; then
      continue
    fi
    REPOS+=("$d")
  done
else
  for d in "$@"; do
    expanded="$(expand "$d")"
    if [[ -d "$expanded/.git" ]]; then
      REPOS+=("$(cd "$expanded" && pwd)")
    else
      echo "Skip (not a git repo): $d" >&2
    fi
  done
fi

if [[ ${#REPOS[@]} -eq 0 ]]; then
  echo "No repos found." >&2
  exit 1
fi

echo "Adding guardrails to ${#REPOS[@]} repo(s):"
for r in "${REPOS[@]}"; do echo "  - $r"; done
echo ""

for repo in "${REPOS[@]}"; do
  name="$(basename "$repo")"
  echo "--- $name ---"
  (
    cd "$repo"
    if [[ -d ".cursor-guardrails" ]]; then
      echo "  Guardrails already present; running install only."
      bash .cursor-guardrails/install.sh
    elif [[ "$USE_LOCAL" == true ]]; then
      echo "  Copying guardrails from local repo (--local)."
      cp -R "$GUARDRAILS_REPO_ROOT" .cursor-guardrails
      rm -rf .cursor-guardrails/.git
      bash .cursor-guardrails/install.sh
      echo "  Local copy added. Commit with: git add .cursor-guardrails .cursor/rules && git commit -m 'chore: add shared Cursor guardrails (local)'"
    else
      git submodule add --force "$GUARDRAILS_URL" .cursor-guardrails
      bash .cursor-guardrails/install.sh
      echo "  Submodule added. Commit with: git add .gitmodules .cursor-guardrails .cursor/rules && git commit -m 'chore: add shared Cursor guardrails'"
    fi
  )
  echo ""
done

echo "Done. Remember to commit and push in each repo if you added the submodule."
