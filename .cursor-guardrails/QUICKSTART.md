# Quick start

## All repos at once (automatic)

```bash
cd /path/to/cursor-guardrails
# If repos already cloned under e.g. ~/github/jobk84092:
bash scripts/add-to-all-repos.sh ~/github/jobk84092
# Or clone all then add guardrails:
bash scripts/clone-and-add-all.sh ~/github/jobk84092 jobk84092
```

## Existing repo (one-time)

```bash
cd /path/to/your/repo
git submodule add https://github.com/jobk84092/cursor-guardrails.git .cursor-guardrails
bash .cursor-guardrails/install.sh
git add .gitmodules .cursor-guardrails .cursor/rules
git commit -m "chore: add shared Cursor guardrails"
git push
```

## New repo (first steps after git init or clone)

```bash
git submodule add https://github.com/jobk84092/cursor-guardrails.git .cursor-guardrails
bash .cursor-guardrails/install.sh
git add .gitmodules .cursor-guardrails .cursor/rules
git commit -m "chore: add shared Cursor guardrails"
```

## Update guardrails in a repo

```bash
git submodule update --remote .cursor-guardrails
bash .cursor-guardrails/install.sh
git add .cursor-guardrails
git commit -m "chore: update cursor-guardrails"
```

---

Replace `jobk84092/cursor-guardrails` with your actual GitHub org/repo if different.
