# Agent Protocols Temp Doc Governance

- Date: 2026-03-30
- Status: in progress
- Scope: cross-repo
- Baseline: `main` at `4ae2656`
- Branch: `feature/agent-protocols/temp-doc-governance-2026-03-30`
- Related ADR: none
- Supersedes: none

## Goal

Add a portable `docs/temp/` lifecycle to the package, document namespaced
branch/worktree/temp-doc conventions that reduce branch sprawl, and prove that
the updated package can be re-vendored into `ironclaw-core` and
`ironclaw-leam` via the installer.

## Phases

### Phase `package_policy`

- Goal: add the canonical temp-doc and naming rules to the package itself.
- Write scope:
  - `README.md`
  - `assistant-*.md`
  - `plan-protocol.md`
  - `proposal-protocol.md`
  - `substantive-work-protocol.md`
  - `temp-doc-protocol.md`
  - `scripts/install.py`
  - `docs/`
- Checks:
  - the package ships `temp-doc-protocol.md`
  - the example docs tree includes `docs/temp/README.md`
  - the installer scaffolds `docs/temp/README.md`
- Exit gate:
  - the package canon consistently explains when temporary notes stay in
    `docs/temp/` versus when they must be promoted into durable docs

### Phase `consumer_refresh`

- Goal: prove the updated package upgrades cleanly in Core and Leam.
- Write scope:
  - vendored `agent-protocols/` in `ironclaw-core`
  - vendored `agent-protocols/` in `ironclaw-leam`
  - installer-scaffolded `docs/temp/README.md` in each consumer repo if absent
- Checks:
  - rerunning the installer refreshes the vendored package in both repos
  - both consumer repos gain the new temp-doc surface without duplicating
    canonical protocol docs elsewhere
- Exit gate:
  - the installer-based upgrade path is proven in both repos

### Phase `acceptance`

- Goal: validate the package scripts and the refreshed consumer installs.
- Checks:
  - package scripts compile
  - the example manifest remains green
  - the refreshed vendored copies in Core and Leam compile
- Exit gate:
  - the phase checker passes for `acceptance`
