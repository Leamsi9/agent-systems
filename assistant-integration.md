# Assistant Integration

This package only works reliably when the consuming repo exposes it through the
instruction surfaces that local assistants already read.

## Discovery Contract

Keep one reusable package and point assistant-specific entrypoints at it.

Recommended approach:

1. vendor the package as `agent-systems/`
2. keep repo topology in a repo-local `agent-systems.toml`
3. point assistant instruction files at
   `agent-systems/substantive-work-protocol.md`
4. keep repo-specific landing pages, ledgers, ADRs, and proposal logs outside
   the vendored package

Do not fork the protocol docs into separate copies for each assistant.

## Minimal Entry Points

At minimum, wire one or more repo instruction files to the package:

- `AGENTS.md`
- `CLAUDE.md`
- any assistant-specific rule or instruction surface your toolchain supports

Those files should stay short and point back to the package instead of
duplicating it.

## Suggested Pointer Text

Use a short pointer such as:

```md
For substantive work, follow `agent-systems/substantive-work-protocol.md`.
Repo topology and linked repos are declared in `agent-systems.toml`.
```

## Bootstrap Help

The package installer can vendor the package, create the config file, and
scaffold the docs skeleton for a new repo:

```bash
python3 agent-systems/scripts/install.py --target . --repo-id my-repo
```

For linked repos that should resolve relative to the git common root instead of
the config file location:

```bash
python3 agent-systems/scripts/install.py --target . --repo-id my-repo --linked-repo workspace@git_common_root=../workspace
```

To print short assistant pointer snippets after scaffolding:

```bash
python3 agent-systems/scripts/install.py --target . --repo-id my-repo --print-assistant-snippets
```

## Upstreaming Rule

If a change to the vendored package is generic, upstream it to the package repo
instead of keeping it as a permanent consumer-only fork.
