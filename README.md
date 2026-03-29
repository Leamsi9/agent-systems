# Agent Systems

This package is a reusable, repo-agnostic protocol kit for agent-driven
planning, proposal capture, phase gates, and live workstream auditing.

It is designed to work in either of these shapes:

- as the root of the public `agent-systems` package repo
- as an `agent-systems/` folder vendored into another repo

Canonical upstream repo:

- `https://github.com/Leamsi9/agent-systems`

## Package Files

- `README.md`
  Package overview and vendoring guidance.
- `VERSION`
  Human-readable package version for vendored copies.
- `SYNCING.md`
  Recommended strategies for propagating upstream improvements into vendored
  instances.
- `substantive-work-protocol.md`
  Canonical workflow for non-trivial implementation work.
- `proposal-protocol.md`
  Canonical workflow for proposal-only slices that stop before implementation.
- `plan-protocol.md`
  Canonical conventions for a repo-local `docs/plans/` surface.
- `examples/gated-phase-manifest.example.toml`
  Reusable example manifest for gated mini-plans.
- `scripts/check_gated_plan.py`
  Canonical phase-checker implementation.
- `scripts/workstream.py`
  Canonical live-workstream audit and status-ledger sync script.

## Vendoring

To vendor this package into another repo:

1. Copy this package into the repo root as `agent-systems/`.
2. Point maintainer docs such as `AGENTS.md` or `CLAUDE.md` to
   `agent-systems/substantive-work-protocol.md`.
3. Add a short `docs/plans/README.md` landing page plus a
   `docs/plans/plans-index.md` inventory.
4. Keep live generated status in a repo-local ledger such as
   `docs/live-workstream-status.md`.
5. Run the canonical scripts directly:
   - `python3 agent-systems/scripts/check_gated_plan.py path/to/work.plan.toml --phase phase_name`
   - `python3 agent-systems/scripts/workstream.py sync-index --confirm`

## Recommended Repo-Local Shape

If a repo adopts the default taxonomy described by this package, it should
normally keep:

- `docs/plans/README.md`
  Short landing page describing what lives in the plans folder.
- `docs/plans/plans-index.md`
  Durable plan inventory and taxonomy index.
- `docs/plans/proposals/{active,pending,blocked,in-progress}/`
  Proposal-only plan families.
- `docs/proposals/{active,pending,blocked,in-progress,archive}/`
  Proposal logs.
- `docs/live-workstream-status.md`
  Script-owned current-state ledger.

The goal is one reusable canonical package and no duplicate authorities.
