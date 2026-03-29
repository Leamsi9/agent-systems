# Live Workstream Status

This ledger is the repo-local mutable current-state surface for active
workstreams, preserved pending proposals, and other manifest-backed plan
families.

## Definitions

- A manifest is a `.plan.toml` phase-gate file paired with a durable plan.
- Manifests are not proposals by default.
- Pending proposals are branchless plan families whose plan records
  `Proposal state: pending`.
- Branchless Plan Manifests are manifest-backed plan families whose recorded
  branch is not currently present locally and that are not classified as
  pending proposals.

Refresh this ledger with:

- `python3 scripts/workstream.py sync-index --confirm`

<!-- BEGIN GENERATED WORKSTREAM STATE -->
## Generated Status Snapshot

This section is generated from live git and worktree state by the agent-systems workstream script.

_Last generated: 2026-03-29T16:10:25.912574+00:00_

### Summary
| Repo | Main | Non-main branches | Attached worktrees | Dirty worktrees |
| --- | --- | --- | --- | --- |
| agent-systems | main | 0 | 1 | 0 |

### Active, Promotable, And Diverged Branches
None.

### Historical And Merged-Stale Branches
None.

### Pending Proposals Without Live Branches
None.

### Branchless Plan Manifests
None.
<!-- END GENERATED WORKSTREAM STATE -->
