# Live Workstream Status

This ledger is the repo-local mutable current-state surface for active
workstreams, manifest-backed pending proposals, and other manifest-backed plan
families. Compact proposal records without manifests remain valid durable docs
but may not appear in this generated ledger.

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

This section is generated from live git and worktree state by the agent-protocols workstream script.

_Last generated: 2026-03-30T07:53:08.378148+00:00_

### Summary
| Repo | Main | Non-main branches | Attached worktrees | Dirty worktrees |
| --- | --- | --- | --- | --- |
| agent-protocols | main | 1 | 2 | 1 |

### Active, Promotable, And Diverged Branches
None.

### Historical And Merged-Stale Branches
| Repo | Branch | Class | Worktree | State | Ahead | Behind | Plan |
| --- | --- | --- | --- | --- | --- | --- | --- |
| agent-protocols | feature/agent-protocols/temp-doc-governance-2026-03-30 | merged_stale | agent-protocols-temp-doc-governance | dirty | - | - | [agent-protocols-temp-doc-governance-2026-03-30.md](/home/ismael/Github/.worktrees/agent-protocols-temp-doc-governance/docs/plans/cross-repo/feature/agent-protocols-temp-doc-governance-2026-03-30.md) |

### Pending Proposals Without Live Branches
None.

### Branchless Plan Manifests
None.
<!-- END GENERATED WORKSTREAM STATE -->
