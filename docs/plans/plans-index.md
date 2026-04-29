# Plans Index

This directory stores durable plan families for the consuming repo.

The canonical reusable planning guidance lives in:

- [Agent protocols plan protocol](../../plan-protocol.md)

Live branch and worktree state is tracked separately in:

- [Live workstream status ledger](../live-workstream-status.md)

## Taxonomy

Use these stable subdirectories:

- `feature/` for product or engineering feature plans
- `sync/` for upstream sync or convergence plans
- `hotfix/` for urgent corrective plans
- `proposals/` for proposal-only plan families
- `archive/` for parked, superseded, promoted, or historical plan families
- `cross-repo/` as an orchestrator-only extension for canonical plan families
  whose completion or acceptance depends on coordinated work across 2+ repos

Within `docs/plans/proposals/`, use explicit status buckets:

- `active/`
- `pending/`
- `blocked/`
- `in-progress/`

A `.plan.toml` manifest is a phase-gate artifact paired with a durable plan. It
is not the same thing as a proposal log. Proposal logs live under
`docs/proposals/`.

## Durable Plan Surfaces

### `feature/`

- [Example workstream](feature/example-workstream.md)

### `sync/`

- [Minor work protocol package sync, 2026-04-29](sync/2026-04-29-minor-work-protocol-package-sync.md)

### `hotfix/`

None.

### `proposals/active`

None.

### `proposals/pending`

None.

### `proposals/blocked`

None.

### `archive/`

None.

### `cross-repo/`

- [Cross-repo extension README](cross-repo/README.md)
