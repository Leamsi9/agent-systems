# Minor Work Protocol Package Sync

- Date: 2026-04-29
- Status: active
- Branch: `chore/minor-work-protocol-package-sync-2026-04-29`
- Baseline: `origin/main` at `4d18a8a`

## Goal

Promote the local `agent-protocols` package edits that introduce the minor-work
protocol and related cleanup guidance, then refresh the `ironclaw-core`
vendored package from the canonical package repo.

## Scope

- Package version `0.0.4`
- `minor-work-protocol.md`
- `substantive-work-protocol.md` link to the minor-work protocol
- `proposal-protocol.md` lifecycle clarification
- `scripts/workstream.py` reconciliation command support
- installer vendoring list so consumer repos receive `minor-work-protocol.md`
- `ironclaw-core/agent-protocols/` refresh after package promotion

## Phases

1. Package validation: prove the package has a coherent `0.0.4` source state
   and installer coverage for the new protocol file.
2. Consumer refresh: merge and push the package, then update the
   `ironclaw-core` vendored copy from the package installer.

## Exit Gate

The package branch is merged to `agent-protocols/main`, `origin/main` is
pushed, and `ironclaw-core/agent-protocols/` matches a fresh installer copy of
the package.
