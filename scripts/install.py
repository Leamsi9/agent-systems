#!/usr/bin/env python3
"""Scaffold repo-local agent-systems integration files."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


DEFAULT_LEDGER_PATH = Path("docs/live-workstream-status.md")
VENDORED_FILES = [
    "README.md",
    "VERSION",
    "SYNCING.md",
    "assistant-integration.md",
    "substantive-work-protocol.md",
    "proposal-protocol.md",
    "plan-protocol.md",
]
OPTIONAL_VENDORED_FILES = [
    "LICENSE-MIT",
    "LICENSE-APACHE",
]
VENDORED_DIRS = [
    "examples",
    "scripts",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold repo-local agent-systems config and docs."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path("."),
        help="Target repo root to scaffold.",
    )
    parser.add_argument(
        "--repo-id",
        help="Primary repo id. Defaults to the target directory name.",
    )
    parser.add_argument(
        "--main-branch",
        default="main",
        help="Primary integration branch for the root repo.",
    )
    parser.add_argument(
        "--linked-repo",
        action="append",
        default=[],
        metavar="ID=PATH",
        help=(
            "Additional linked repo entries to add to agent-systems.toml. "
            "Use ID=PATH for config-root-relative repos or "
            "ID@git_common_root=PATH for worktree-aware sibling repos."
        ),
    )
    parser.add_argument(
        "--print-assistant-snippets",
        action="store_true",
        help="Print short assistant entrypoint snippets after scaffolding.",
    )
    parser.add_argument(
        "--vendor-dir",
        default="agent-systems",
        help="Directory name to use when vendoring the package into the target repo.",
    )
    return parser.parse_args()


def parse_linked_repo(spec: str) -> tuple[str, str, str]:
    if "=" not in spec:
        raise ValueError(f"invalid linked repo '{spec}', expected ID=PATH")
    repo_token, repo_path = spec.split("=", 1)
    repo_token = repo_token.strip()
    repo_path = repo_path.strip()
    if not repo_token or not repo_path:
        raise ValueError(f"invalid linked repo '{spec}', expected ID=PATH")
    repo_id = repo_token
    path_base = "config_root"
    if "@" in repo_token:
        repo_id, path_base = repo_token.split("@", 1)
        repo_id = repo_id.strip()
        path_base = path_base.strip()
    if not repo_id:
        raise ValueError(f"invalid linked repo '{spec}', missing repo id")
    if path_base not in {"config_root", "git_common_root"}:
        raise ValueError(
            f"invalid linked repo '{spec}', unsupported path base '{path_base}'"
        )
    return repo_id, repo_path, path_base


def write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def package_root() -> Path:
    return Path(__file__).resolve().parent.parent


def copy_package(source_root: Path, target_root: Path, vendor_dir: str) -> Path:
    vendor_root = (target_root / vendor_dir).resolve()
    if vendor_root == source_root.resolve():
        return vendor_root

    vendor_root.mkdir(parents=True, exist_ok=True)

    for relative in VENDORED_FILES:
        source = source_root / relative
        destination = vendor_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    for relative in OPTIONAL_VENDORED_FILES:
        source = source_root / relative
        if not source.exists():
            continue
        destination = vendor_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    for relative in VENDORED_DIRS:
        source = source_root / relative
        destination = vendor_root / relative
        shutil.copytree(source, destination, dirs_exist_ok=True)

    return vendor_root


def build_config(
    repo_id: str,
    main_branch: str,
    linked_repos: list[tuple[str, str, str]],
) -> str:
    lines = [
        'version = 1',
        f'status_ledger_path = "{DEFAULT_LEDGER_PATH.as_posix()}"',
        "",
        "[[repos]]",
        f'id = "{repo_id}"',
        'path = "."',
        f'main_branch = "{main_branch}"',
    ]
    for linked_id, linked_path, linked_path_base in linked_repos:
        lines.extend(
            [
                "",
                "[[repos]]",
                f'id = "{linked_id}"',
                f'path = "{linked_path}"',
            ]
        )
        if linked_path_base != "config_root":
            lines.append(f'path_base = "{linked_path_base}"')
        lines.append(f'main_branch = "{main_branch}"')
    lines.append("")
    return "\n".join(lines)


def plans_readme() -> str:
    return """# Plans

This folder stores durable plan families for this repo.

This `README.md` is only the landing page. The durable inventory lives in
`docs/plans/plans-index.md`.

Start here:

- `docs/plans/plans-index.md`
- `docs/live-workstream-status.md`
- `agent-systems/substantive-work-protocol.md`
- `agent-systems/proposal-protocol.md`
"""


def plans_index() -> str:
    return """# Plans Index

This directory stores durable plan families for this repo.

The canonical reusable planning guidance lives in:

- `agent-systems/plan-protocol.md`

Live branch and worktree state is tracked separately in:

- `docs/live-workstream-status.md`

## Taxonomy

- `feature/`
- `sync/`
- `hotfix/`
- `proposals/`
- `archive/`
"""


def live_ledger() -> str:
    return """# Live Workstream Status

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

- `python3 agent-systems/scripts/workstream.py sync-index --confirm`

<!-- BEGIN GENERATED WORKSTREAM STATE -->
Template placeholder.
<!-- END GENERATED WORKSTREAM STATE -->
"""


def proposals_readme() -> str:
    return """# Proposal Logs

This folder is the default proposal-log surface for repos that adopt the
proposal protocol.
"""


def pending_adr_readme() -> str:
    return """# Pending ADRs

This folder stores proposal-stage ADRs that are not accepted yet.
"""


def example_plan() -> str:
    return """# Example Workstream

- Date: 2026-03-29
- Status: template
- Scope: example-only plan family for package consumers
- Baseline: example only
- Branch: none (template example)
- Related ADR: none
- Supersedes: none
"""


def example_manifest() -> str:
    return """title = "Example workstream"
root_dir = "../../.."
completion_ledger = "docs/plans/feature/example-workstream-completion.md"
phase_order = ["setup", "acceptance"]

[phases.setup]
summary = "Ensure the example plan family is present."

[[phases.setup.checks]]
id = "plan-exists"
type = "path_exists"
path = "docs/plans/feature/example-workstream.md"

[[phases.setup.checks]]
id = "manifest-exists"
type = "path_exists"
path = "docs/plans/feature/example-workstream.plan.toml"

[[phases.setup.checks]]
id = "completion-log-exists"
type = "path_exists"
path = "docs/plans/feature/example-workstream-completion.md"

[phases.acceptance]
summary = "Validate the example repo skeleton."
depends_on = ["setup"]

[[phases.acceptance.checks]]
id = "plans-readme-links-index"
type = "text_present"
path = "docs/plans/README.md"
text = "docs/plans/plans-index.md"

[[phases.acceptance.checks]]
id = "plans-readme-links-ledger"
type = "text_present"
path = "docs/plans/README.md"
text = "docs/live-workstream-status.md"

[[phases.acceptance.checks]]
id = "scripts-compile"
type = "command"
command = "python3 -m py_compile agent-systems/scripts/check_gated_plan.py agent-systems/scripts/workstream.py"
"""


def example_completion() -> str:
    return """# Example Workstream Completion Log

- Date: 2026-03-29
- Status: template
- Branch: none (template example)
"""


def scaffold(
    target: Path,
    repo_id: str,
    main_branch: str,
    linked_repos: list[tuple[str, str, str]],
    vendor_dir: str,
) -> None:
    target.mkdir(parents=True, exist_ok=True)
    copy_package(package_root(), target, vendor_dir)
    write_if_missing(
        target / "agent-systems.toml",
        build_config(repo_id=repo_id, main_branch=main_branch, linked_repos=linked_repos),
    )

    for relative in [
        "docs/plans/feature",
        "docs/plans/hotfix",
        "docs/plans/sync",
        "docs/plans/archive",
        "docs/plans/proposals/active",
        "docs/plans/proposals/pending",
        "docs/plans/proposals/blocked",
        "docs/plans/proposals/in-progress",
        "docs/proposals/active",
        "docs/proposals/pending",
        "docs/proposals/blocked",
        "docs/proposals/in-progress",
        "docs/proposals/archive",
        "docs/adr/pending",
    ]:
        (target / relative).mkdir(parents=True, exist_ok=True)

    write_if_missing(target / "docs/plans/README.md", plans_readme())
    write_if_missing(target / "docs/plans/plans-index.md", plans_index())
    write_if_missing(target / DEFAULT_LEDGER_PATH, live_ledger())
    write_if_missing(target / "docs/proposals/README.md", proposals_readme())
    write_if_missing(target / "docs/adr/pending/README.md", pending_adr_readme())
    write_if_missing(target / "docs/plans/feature/example-workstream.md", example_plan())
    write_if_missing(
        target / "docs/plans/feature/example-workstream.plan.toml",
        example_manifest(),
    )
    write_if_missing(
        target / "docs/plans/feature/example-workstream-completion.md",
        example_completion(),
    )


def print_assistant_snippets() -> None:
    snippet = (
        "For substantive work, follow `agent-systems/substantive-work-protocol.md`.\n"
        "Repo topology and linked repos are declared in `agent-systems.toml`.\n"
    )
    print("AGENTS.md / CLAUDE.md snippet:\n")
    print(snippet)


def main() -> int:
    args = parse_args()
    target = args.target.resolve()
    repo_id = args.repo_id or target.name
    linked_repos = [parse_linked_repo(spec) for spec in args.linked_repo]
    scaffold(
        target=target,
        repo_id=repo_id,
        main_branch=args.main_branch,
        linked_repos=linked_repos,
        vendor_dir=args.vendor_dir,
    )
    print(f"scaffolded agent-systems integration in {target}")
    if args.print_assistant_snippets:
        print()
        print_assistant_snippets()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
