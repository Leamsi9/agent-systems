# Proposal Protocol

Use this protocol when a change is important enough to preserve durably, but it
is not ready to implement or accept yet.

Proposal slices still follow the
[Substantive work protocol](substantive-work-protocol.md) for branch
discipline, phase gates, and completion evidence.

## When To Use This

Use the proposal protocol when any of these are true:

- the workstream stops at a durable proposal rather than implementation
- the architecture direction is useful to preserve, but not ready to accept
- the change needs a reviewable proposal artifact in one or more repos
- you want later chats to resume from durable repo state instead of chat memory

## Required Artifacts

Every proposal workstream should keep:

1. a durable plan in `docs/plans/proposals/`
2. an adjacent `.plan.toml` manifest
3. an append-only completion log
4. a pending ADR in the owning repo when the slice preserves an architecture
   decision
5. a proposal log in each repo that owns a concrete pending target

## Canonical Locations

### Proposal Plan Families

Use explicit status buckets under `docs/plans/proposals/`:

- `active/`
- `pending/`
- `blocked/`
- `in-progress/`

Historical proposal plan families move to `docs/plans/archive/`.

### Pending ADRs

- accepted ADRs stay in `docs/adr/`
- pending ADRs live in `docs/adr/pending/`
- do not keep pending ADRs in the accepted ADR namespace

### Proposal Logs

Use the proposal-log surface owned by the repo that owns the pending target.

When a repo uses the default layout, keep explicit status buckets under
`docs/proposals/`:

- `active/`
- `pending/`
- `blocked/`
- `in-progress/`
- `archive/`

Do not create duplicate proposal logs in both repos unless both repos have
their own concrete owned targets.

## Manifest Vs Proposal

A manifest is a `.plan.toml` gate file for a plan family. It is not the same
thing as a proposal.

A proposal is the full pending workstream record:

- the proposal plan family
- the manifest
- the completion log
- any pending ADR
- the proposal log

Pending proposals are therefore a subset of manifest-backed plan families, not
the whole set.

## Proposal Visibility

Pending proposals are part of current-state visibility, but they do not belong
inside a `README`.

Keep the durable proposal plan family in `docs/plans/proposals/`, keep the
pending ADR and proposal log in their owned locations, and let a script-owned
ledger such as `docs/live-workstream-status.md` surface the proposal as
`pending_proposal` when it is preserved on the integration branch without a
live implementation branch.

## Ownership Rules

For cross-repo proposal work, use these defaults:

- one canonical plan family
- one pending ADR in the repo that owns the architecture decision
- one proposal log per repo only when that repo owns a real pending target
- thin mirrors instead of duplicate narrative copies

Examples:

- shared runtime proposal:
  - plan in the shared repo
  - pending ADR in the shared repo
  - proposal log in the shared repo
- product- or workspace-owned proposal:
  - plan in the canonical planning repo when the work is cross-repo
  - pending ADR in the repo that owns the architecture decision, when needed
  - proposal log in the product- or workspace-owned review surface
- cross-repo implementation idea with no concrete product-owned target yet:
  - keep the plan plus pending ADR in the shared repo
  - keep one proposal log in the shared repo

## Proposal Log Content

A proposal log should record:

- status
- proposal class
- owning repo and target surface
- related plan path
- pending ADR path when applicable
- the proposed change in a compact, reviewable form

If the proposal log uses an existing typed contract, keep using that contract
instead of inventing a second one.

## Lifecycle

The intended lifecycle is:

1. create the dedicated branch and durable proposal artifacts
2. capture the pending direction in the proposal plan family
3. capture the pending ADR in `docs/adr/pending/` when needed
4. capture the proposal log in the owning repo
5. merge the proposal slice to the integration baseline
6. later either:
   - resume it as a fresh implementation workstream, or
   - archive it as superseded or rejected

When a proposal is accepted later:

- promote the accepted ADR into `docs/adr/`
- archive the old pending ADR path
- archive or update the proposal log according to the owning repo’s review
  contract
- archive the old proposal-plan family when it is no longer live

## Archive Vs History

- `docs/plans/archive/` is for historical proposal plan families
- `docs/history/` is for factual ledgers and preserved records
- `docs/proposals/archive/` is for historical proposal logs when the repo keeps
  proposal logs under `docs/proposals/`

Do not move proposal plans or pending ADRs into `docs/history/` just because
they are no longer active. Use archive paths for inactive planning artifacts
and history paths for factual records.
