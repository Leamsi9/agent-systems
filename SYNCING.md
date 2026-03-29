# Syncing

This package is meant to be vendored into other repos without forking the
protocol logic by hand.

## Recommended Strategy

Use a dedicated upstream repo plus a vendored folder in consumers.

Recommended flow:

1. publish and tag releases in `https://github.com/Leamsi9/agent-protocols`
2. vendor the package into consumer repos as `agent-protocols/`
3. keep a `VERSION` file inside the vendored copy
4. update consumers by copying a tagged release or by pulling a subtree update

The package is intentionally staying on `0.0.x` until the config contract and
Leam adoption are proven stable.

## Compatibility Contract

Treat the package directory structure and canonical filenames as a compatibility
surface.

- adding new protocols, examples, or scripts is normally safe
- moving or renaming canonical files is a breaking change for consumers
- while the package is still on `0.0.x`, avoid layout churn unless the gain is
  clear and the migration notes are ready

## Good Import Options

- `git subtree`
  Best fit when you want one external history source but do not want submodule
  friction in day-to-day work.
- release tarball or tagged copy
  Best fit when consumers are not all using Git in the same way.
- manual copy with version bump
  Acceptable for smaller repos, but only if the `VERSION` file is updated and
  the sync source is recorded in the consuming repo.

## Minimal Consumer Contract

Each consumer should document:

- the upstream repo URL
- the vendored package version
- the local owner of repo-specific overlays outside the package

Keep reusable protocol content in the package. Keep repo-specific landing
pages, ledgers, ADRs, and proposal logs in the consuming repo.

## Upstream First For Generic Changes

If a consumer repo discovers a generic improvement:

1. implement and validate it locally
2. open a branch or PR against `Leamsi9/agent-protocols`
3. then sync the resulting upstream package change back into consumers

Do not let long-lived consumer-only package forks become the default workflow.
