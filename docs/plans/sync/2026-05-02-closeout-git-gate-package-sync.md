# Closeout Git Gate Package Sync, 2026-05-02

## Goal

Make the package canonical for final git closeout evidence across substantive
manifests and delegated jobs.

## Baseline

- integration branch: `main`
- baseline commit: `9a6eb47488b5814bc4be7aeed2a5e9958d23161b`
- package branch: `feature/closeout-git-gate-2026-05-02`

## Write Scope

- `substantive-work-protocol.md`
- `delegated-work-protocol.md`
- `scripts/check_gated_plan.py`
- `examples/gated-phase-manifest.example.toml`
- package metadata and vendoring lists

## Phases

1. Add final git checkpoint requirements to the package protocols.
2. Add manifest support and examples for proving `HEAD` is ahead of baseline.
3. Refresh the consumer copy in `ironclaw-core` from the updated package.

## Exit Gate

The package branch must pass the manifest checker, be committed with `HEAD`
ahead of the recorded baseline, and vendor cleanly into `ironclaw-core`.
