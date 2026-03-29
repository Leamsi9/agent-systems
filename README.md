# Agent Protocols

Experimental package version: `0.0.1`

This package is a reusable, repo-agnostic protocol kit for agent-driven
planning, proposal capture, phase gates, and live workstream auditing.

It is designed to work in either of these shapes:

- as the root of the public `agent-protocols` package repo
- as an `agent-protocols/` folder vendored into another repo

Canonical upstream repo:

- `https://github.com/Leamsi9/agent-protocols`

## Package Files

- `README.md`
  Package overview and vendoring guidance.
- `VERSION`
  Human-readable package version for vendored copies.
- `SYNCING.md`
  Recommended strategies for propagating upstream improvements into vendored
  instances.
- `assistant-integration.md`
  Guidance for wiring repo instruction surfaces back to the package.
- `assistant-adoption-prompt.md`
  Copy-paste prompt template for asking a coding assistant to adopt the package
  in another repo.
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
- `scripts/install.py`
  Bootstrap installer that vendors the package and scaffolds repo-local config
  and docs.

## Standalone Quick Start

The public package repo ships a small example `docs/` skeleton so you can
validate the package in isolation:

- `python3 scripts/check_gated_plan.py docs/plans/feature/example-workstream.plan.toml --phase acceptance`
- `python3 scripts/workstream.py sync-index --confirm`

To vendor the package into a fresh repo and scaffold the repo-local layout:

- `python3 scripts/install.py --target /path/to/repo --repo-id my-repo`
- `python3 scripts/install.py --target /path/to/repo --repo-id my-repo --linked-repo workspace@git_common_root=../workspace`
- `python3 scripts/install.py --target /path/to/repo --repo-id my-repo --print-adoption-prompt`

## Vendoring

To vendor this package into another repo:

1. Copy this package into the repo root as `agent-protocols/`.
2. Generate or maintain a repo-local `agent-protocols.toml` that declares the
   owning repo and any linked repos.
3. Point maintainer docs such as `AGENTS.md` or `CLAUDE.md` to
   `agent-protocols/substantive-work-protocol.md`.
4. Add a short `docs/plans/README.md` landing page plus a
   `docs/plans/plans-index.md` inventory.
5. Keep live generated status in a repo-local ledger such as
   `docs/live-workstream-status.md`.
6. Run the canonical scripts directly:
   - `python3 agent-protocols/scripts/check_gated_plan.py path/to/work.plan.toml --phase phase_name`
   - `python3 agent-protocols/scripts/workstream.py sync-index --confirm`
   - `python3 agent-protocols/scripts/install.py --target . --repo-id my-repo`

See also:

- `examples/repo-config.example.toml`
- `assistant-integration.md`
- `assistant-adoption-prompt.md`

## Compatibility Surface

Treat the package path layout and canonical filenames as part of the package
interface.

- additive protocols, examples, or scripts are the safe default
- moved or renamed canonical files should ship with an explicit migration note
- consumer repos should update active references before pruning historical docs

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
