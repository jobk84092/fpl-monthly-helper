# Cursor Guardrails — No hallucination across all repos

Shared Cursor rules and prompts so **every repo** (existing and future) uses the same “no hallucination” and analytics guardrails.

## How it works

- This repo is the **single source of truth** for rules and prompts.
- Each project (existing or new) either **submodules** this repo or **copies** it in, then runs the install step so Cursor sees the rules.
- Works for: **automatic-jobs**, **docker-bootcamp**, **DSBA-Class-practice**, **football-jackpot-prediction**, **fpl-monthly-helper**, **model-deployment**, and any **new repo** you create.

---

## Option A: Add to an existing repo

From the **root of the existing repo** (e.g. `automatic-jobs`, `football-jackpot-prediction`):

```bash
# 1. Add this guardrails repo as a submodule (fixed path so scripts stay the same)
git submodule add https://github.com/jobk84092/cursor-guardrails.git .cursor-guardrails

# 2. Install rules into this project's .cursor/rules (so Cursor loads them)
bash .cursor-guardrails/install.sh
```

Then commit the submodule and the new `.cursor/rules` content:

```bash
git add .gitmodules .cursor-guardrails .cursor/rules
git commit -m "chore: add shared Cursor guardrails (no-hallucination)"
git push
```

---

## Option B: New repo from scratch

When you **create a new repo**, do this after the first `git init` or clone:

```bash
git submodule add https://github.com/jobk84092/cursor-guardrails.git .cursor-guardrails
bash .cursor-guardrails/install.sh
git add .gitmodules .cursor-guardrails .cursor/rules
git commit -m "chore: add shared Cursor guardrails"
```

---

## Option C: Clone a repo that already has the submodule

If someone (or you) already added the submodule:

```bash
git clone --recurse-submodules https://github.com/jobk84092/<repo>.git
cd <repo>
bash .cursor-guardrails/install.sh
```

If you already cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
bash .cursor-guardrails/install.sh
```

---

## Updating guardrails in all repos

After you change this repo (e.g. new rules or prompts):

```bash
# In each project that uses the submodule:
cd /path/to/any/repo
git submodule update --remote .cursor-guardrails
bash .cursor-guardrails/install.sh
```

Then commit the updated submodule ref in that repo.

---

## Add to all repos automatically

From the **cursor-guardrails** repo root:

**If you already have all repos cloned** (e.g. under `~/github/jobk84092`):

```bash
cd /path/to/cursor-guardrails
bash scripts/add-to-all-repos.sh ~/github/jobk84092
```

This finds every git repo in that directory, adds the `.cursor-guardrails` submodule (if missing), and runs `install.sh` in each. Then commit and push in each repo.

**If you want to clone all repos and add guardrails in one go:**

```bash
cd /path/to/cursor-guardrails
bash scripts/clone-and-add-all.sh ~/github/jobk84092 jobk84092
```

This clones every repo listed in `scripts/repos.txt` into the target directory, then runs `add-to-all-repos.sh` on it. Edit `scripts/repos.txt` to add or remove repo names.

**Add guardrails to a custom list of repo paths:**

```bash
bash scripts/add-to-all-repos.sh /path/to/repo1 /path/to/repo2 /path/to/repo3
```

---

## What gets installed

| Source (this repo)           | Installed into project           |
|-----------------------------|----------------------------------|
| `rules/no-hallucination.mdc`    | `.cursor/rules/no-hallucination.mdc`    |
| `rules/analytics-copilot.mdc`   | `.cursor/rules/analytics-copilot.mdc`   |
| `rules/validation-checklist.mdc` | `.cursor/rules/validation-checklist.mdc` |
| `prompts/` (reference)       | Not copied; link from rules if needed   |

Cursor loads everything in `.cursor/rules/`, so every project gets the same behavior, including the **validation checklist** (must pass before sharing any metric).

---

## Repos covered

The automatic scripts use `scripts/repos.txt`, which lists: **automatic-jobs**, **docker-bootcamp**, **DSBA-Class-practice**, **football-jackpot-prediction**, **fpl-monthly-helper**, **model-deployment**. Add new repo names there so they are included next time you run `clone-and-add-all.sh` or so you can add guardrails to new clones with `add-to-all-repos.sh`.

---

## Without Git submodule (copy once)

If you prefer not to use submodules, clone this repo once and point the install script at it:

```bash
git clone https://github.com/jobk84092/cursor-guardrails.git /path/to/cursor-guardrails
# From each project root:
/path/to/cursor-guardrails/install.sh --source /path/to/cursor-guardrails
```

You can also copy the contents of `rules/` into each project’s `.cursor/rules/` by hand; then you must update each repo when you change the guardrails.
