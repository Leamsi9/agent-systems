# Example Workstream

- Date: 2026-03-29
- Status: template
- Scope: example-only plan family for package consumers
- Baseline: example only
- Branch: none (template example)
- Related ADR: none
- Supersedes: none

## Goal

Provide one concrete example of the expected plan-family shape without shipping
real product history in the package repo.

## Phases

### Phase `setup`

- Goal: ensure the example plan family is present.
- Exit gate:
  - the example plan and manifest exist

### Phase `acceptance`

- Goal: prove the example package layout is internally consistent.
- Exit gate:
  - the plans landing page points at the inventory and live ledger
  - the package scripts compile cleanly
