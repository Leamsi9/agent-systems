# Minor Work Protocol

This is the lightweight workflow for changes that do not warrant the
[Substantive work protocol](substantive-work-protocol.md) but are still worth
treating with explicit, repeatable discipline.

Use it for tiny edits, isolated fixes, single-file tweaks, dependency bumps,
copy adjustments, and one-off cleanups where a full gated mini-plan would be
heavier than the change.

## When To Use This

Use this protocol when all of these are true:

- the change fits in a single reviewable slice
- it does not span repos or ownership boundaries
- it does not introduce, remove, or relocate a public surface, schema, or
  contract
- it has no meaningful product, runtime, or security risk beyond the local
  edit
- the work can plausibly be completed in one short sitting

If any of those stop being true mid-work, stop and escalate to the
[Substantive work protocol](substantive-work-protocol.md). Mid-work
escalation is normal and not a process failure.

## What This Replaces

This protocol replaces the substantive process for genuinely small work.
It does not replace:

- the [Proposal protocol](proposal-protocol.md) when the change captures a
  durable architectural decision
- the [Temp doc protocol](temp-doc-protocol.md) when the work generates
  scratch notes that should be reviewed and deleted
- normal commit hygiene, code review, or test discipline

## Core Rules

1. Prefer a short-lived dedicated branch over committing directly to the
   primary integration branch. Even at small scope a branch keeps the change
   reverting and reviewing cleanly.
2. Direct commits to the integration branch are acceptable for trivial,
   self-contained, and obviously safe edits. Note the reason in the commit
   message when the change is anything more than that.
3. Keep the change focused. If you find yourself touching unrelated files,
   either revert the wandering edits or escalate to the substantive protocol.
4. Land the change on the integration branch in a single reviewable slice.
   Do not split a minor change across multiple branches.
5. Run any normally required checks (lint, format, tests) before merging.
   Minor scope is not a license to skip them.
6. After the change lands, decide whether the decision behind it is worth
   preserving in a durable record. For most minor work the answer is no; for
   some it is yes.

## Lightweight Decision Log

When a minor change reflects a small but durable decision, prefer a one-line
entry in a repo-local decision log over creating a full proposal artifact set.

Recommended shape:

- a single markdown file at `docs/decisions/decision-log.md`, or the path the
  repo already uses for short decisions
- one append-only entry per decision
- format: `YYYY-MM-DD <slug> — one-line decision, optional commit ref`

Do not promote a decision-log entry into a pending ADR or a proposal log
unless the decision crosses the substantive threshold. The whole point of the
log is to capture small decisions without proposal ceremony.

If the repo does not have a decision log and the operator does not want one,
skip this step. Most minor work needs no durable record beyond the commit
message.

## Escalation Triggers

Escalate to the substantive protocol when any of these become true:

- the change starts to span multiple files in different modules with non-local
  effects
- the change touches a public surface, contract, schema, or persisted format
- the change requires more than one reviewable slice
- the work uncovers a separate problem that is not obviously a one-line fix
- the operator or a reviewer asks for a plan, manifest, or completion log

When you escalate, stop committing on the minor branch, treat the work in
progress as early exploration, and recreate the work on a substantive branch
with a durable plan and `.plan.toml` manifest.

## When Not To Use This

Do not use this protocol when the change:

- needs gated phase evidence to be considered done
- spans repos
- needs a pending ADR or proposal log
- is part of a larger workstream that already has a substantive plan
- has even moderate product, runtime, or security risk

In those cases, use the substantive or proposal protocols instead.

## Naming And Branches

When a dedicated branch is used for minor work, prefer a stable shape:

- `chore/<slug>-YYYY-MM-DD`
- `fix/<slug>-YYYY-MM-DD`
- `docs/<slug>-YYYY-MM-DD`

Worktree directories are usually not needed for minor work because the
integration checkout is sufficient and the branch is short-lived. If a
worktree is created, follow the substantive protocol's naming convention.

## Closeout

Closeout for minor work is:

1. ensure the change is on the integration branch and pushed when the repo
   policy expects a remote checkpoint
2. delete the local branch if one was used
3. add a decision-log entry only when the decision is worth preserving

A decision-log entry is not a substitute for substantive completion evidence.
It is a lightweight historical breadcrumb, not a gate.
