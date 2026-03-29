# Substantive Work Protocol

This is the canonical planning and execution workflow for substantive work in a
repo that vendors `agent-systems/`.

Use it for any non-trivial feature, fix, refactor, migration, or cross-repo
change.

If the workstream is intentionally proposal-only and stops before
implementation, pair this protocol with the
[Proposal protocol](proposal-protocol.md).

## When To Use This

This protocol is the default when any of these are true:

- the change spans multiple files or modules
- the work has meaningful product, runtime, or security risk
- the work needs more than one reviewable implementation slice
- the work crosses repos or ownership boundaries
- the user asked for an epic, rollout, or non-trivial implementation plan

For tiny local edits, normal scoped execution is still fine. For substantive
work, use this protocol unless there is a very good reason not to.

## Core Rules

1. Every new feature, functionality change, or fix starts on its own branch.
2. The branch should start from the repo’s primary integration branch.
   The examples in this package assume `main`; if the repo uses another trunk
   branch, record that explicitly in the plan and the checks.
3. If the work spans repos, create a matching branch pair and keep each repo in
   its own worktree.
4. Break the work into an ordered sequence of gated mini-plans instead of one
   giant plan.
5. Only one phase may be actively implemented at a time.
6. Do not advance until the current phase exit gate passes.
7. Do not call work complete from narrative judgement alone. Completion must be
   backed by the phase checker and the documented gate.
8. Merge to the repo’s primary integration branch only after acceptance and
   final-green closure.
9. Treat live git and worktree state as authoritative. Durable docs should
   mirror that state, not override it.
10. Proposal-only slices still need durable artifacts. Use the proposal
    protocol so pending ADRs, proposal logs, and completion traces stay
    predictable.

## Canonical Artifact Set

Substantive work should use these artifacts.

### 1. Durable plan doc

Store the durable workstream plan in `docs/plans/`.

The plan should record:

- the goal
- the baseline branch or commit
- the branch name for the work
- the ordered phases
- the write scope
- the validation and exit gates

### 2. Phase manifest

Store a machine-checkable manifest next to the plan. The recommended suffix is
`.plan.toml`.

A manifest is a phase-gate file paired with a durable plan. A manifest is not
automatically a proposal.

The manifest is the fail-closed source of truth for whether a phase is actually
done.

### 3. Completion log

Store an append-only completion log next to the plan and manifest.

The completion log should capture:

- phase evidence that actually passed
- important SHAs, merges, pushes, and cleanup actions
- remaining work after the finished slice

### 4. Proposal protocol when implementation is intentionally deferred

If the workstream stops at a durable proposal rather than implementation,
follow the [Proposal protocol](proposal-protocol.md) for pending ADR and
proposal-log rules in addition to this protocol.

### 5. Optional per-phase notes

If a phase is large, give it a short companion markdown note near the durable
plan. Keep those notes in `docs/plans/`, not in runtime procedure folders.

### 6. Repo-local mirrors only when needed

If one repo or product owns the canonical plan, other repos should point back
to it and add thin local notes only when they genuinely need companion
guidance.

## Phase Structure

Each phase should be small enough to fit in one working context window and one
reviewable change slice.

Every phase should declare:

- `Goal`
- `Write scope`
- `Dependencies`
- `Checks`
- `Negative assertions`
- `Required docs or ledger updates`
- `Exit gate`

### Checks

Checks prove that the phase landed. Examples:

- targeted tests
- focused validation commands
- file or route existence checks
- content assertions in docs or config

### Negative Assertions

Negative assertions prevent partial migration from being presented as complete.
Examples:

- an old compatibility surface is no longer authoritative
- an obsolete path is gone
- a stale branch name is no longer documented as current

If a phase only proves what is present and never proves what is gone, the gate
is usually too weak.

## Standard Execution Loop

For substantive work, follow this loop every time:

1. Create a dedicated branch from the repo’s integration baseline.
2. If the change spans repos, create a matching branch worktree in each repo.
3. Create or refresh the durable plan and the `.plan.toml` manifest.
4. Load only the current phase, the relevant code, and the required ledgers.
5. Implement only the current phase.
6. Run the phase checker against the current phase.
7. Update docs, completion logs, and mirrors required by that phase.
8. Re-run the phase checker.
9. Advance only when the phase is green.
10. Merge only after acceptance and final-green closure.

## Current-State Ledger

If the repo keeps a live current-state audit, keep one generated repo-local
ledger such as `docs/live-workstream-status.md`.

Do not collapse live mutable branch state into the canonical planning protocol.
The plans landing page, plans index, and live-state ledger have different jobs.

That generated ledger should always be derived from git and worktree
inspection, not hand-maintained from narrative memory.

Pending proposals should appear there as pending proposals. Branchless plan
manifests should appear as branchless plan manifests: manifest-backed plan
families whose recorded branch is not currently present locally, but which are
not automatically proposals.

## Archive And History

Keep these roles distinct:

- `docs/plans/archive/` for historical, promoted, superseded, or parked plan
  families, including their manifests, completion logs, and phase notes
- `docs/history/` for factual ledgers, preserved audits, migration notes,
  branch snapshots, and postmortems

Use `archive` when the artifact is still fundamentally a plan family. Use
`history` when the artifact is a factual record of what happened.

## Context Hygiene

For large streams, the active context should be:

- the current phase doc
- the current manifest
- only the code and specs needed for that phase
- only the review or ledger sections that the phase must update

Do not keep the entire epic live in context if the current phase can be proven
with a smaller working set.

## Checker Contract

Use the canonical checker:

```bash
python3 agent-systems/scripts/check_gated_plan.py path/to/work.plan.toml --phase phase_name
```

Supported check types are illustrated in:

- [gated-phase-manifest.example.toml](examples/gated-phase-manifest.example.toml)

## Minimal Manifest Shape

The manifest is TOML so it can be parsed with the Python standard library.

Use:

- top-level `title`
- optional `branch`
- optional `root_dir`
- ordered `phase_order`
- one `[phases.<name>]` table per phase
- `depends_on` where needed
- one or more `[[phases.<name>.checks]]`

Supported check types:

- `path_exists`
- `path_absent`
- `text_present`
- `text_absent`
- `regex_present`
- `regex_absent`
- `command`
- `git_clean`
- `git_merged_into`
- `git_ref_equals`
- `git_branch_absent`
- `worktree_absent`

## Branch Rule

This rule is mandatory for substantive work:

- do not continue new implementation on whatever branch happened to be checked
  out when the request arrived
- create a fresh dedicated branch for the new workstream
- if the work spans repos, create a matching branch pair
- keep a stable integration worktree available for bootstrap paths and merge
  targets

Planning-system changes are not exempt.

## Merge Rule

The intended lifecycle is:

1. branch from the integration baseline
2. implement behind gated phases
3. accept the work
4. merge back to the integration baseline

If a workstream is parked, superseded, or intentionally left partial, record
that in the durable plan instead of silently leaving the branch as ambiguous
truth.
