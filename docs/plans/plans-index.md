# Plans Index

This directory stores durable plan families for the consuming repo.

The canonical reusable planning guidance lives in:

- [Agent systems plan protocol](../../plan-protocol.md)

Live branch and worktree state is tracked separately in:

- [Live workstream status ledger](../live-workstream-status.md)

## Taxonomy

Use these stable subdirectories:

- `feature/` for product or engineering feature plans
- `sync/` for upstream sync or convergence plans
- `hotfix/` for urgent corrective plans
- `proposals/` for proposal-only plan families
- `archive/` for parked, superseded, promoted, or historical plan families

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

None.

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
