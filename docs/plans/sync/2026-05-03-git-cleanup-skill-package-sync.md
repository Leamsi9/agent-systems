# Git Cleanup Skill Package Sync, 2026-05-03

## Goal

Make `agent-protocols` the canonical home for the git cleanup lifecycle rule,
the deterministic repo-state script, and the reusable `git-cleanup` skill.

## Baseline

- package integration branch: `main`
- package baseline commit: `095f1c9`
- package branch: `feature/git-cleanup-skill-2026-05-03`
- consumer branch: `feature/git-cleanup-skill-vendor-2026-05-03`
- consumer baseline commit: `64200e9a`

## Write Scope

- package `scripts/repo_state.py`
- package `skills/git-cleanup/SKILL.md`
- package installer vendoring lists
- package protocol and integration docs that describe repo-state use
- package tests for repo-state behavior and skill vendoring
- `ironclaw-core` vendored `agent-protocols/` refresh
- temporary Leam projection at `products/leam/skills/git-cleanup/SKILL.md`

## Phases

1. Add package-owned repo-state tooling, the reusable skill, tests, and docs.
2. Refresh the `ironclaw-core` vendored package from the package branch.
3. Copy the package-owned skill into Leam's currently discovered product skill
   surface until Ironclaw has multi-directory skill discovery.

## Exit Gate

The package tests must pass, package scripts must compile, the consumer
vendored copy must include the new script and skill, and both worktrees must
finish clean with committed branch heads ahead of their baselines.
