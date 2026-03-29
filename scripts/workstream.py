#!/usr/bin/env python3
"""Live workstream audit and status-ledger sync for substantive work."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


GENERATED_START = "<!-- BEGIN GENERATED WORKSTREAM STATE -->"
GENERATED_END = "<!-- END GENERATED WORKSTREAM STATE -->"
STATUS_LEDGER_PATH = Path("docs/live-workstream-status.md")
HISTORICAL_PREFIXES = ("backup/", "recovery/", "audit/", "hotfix/", "safety/")
HISTORICAL_NAMES = {"staging"}
STATUS_PATTERN = re.compile(r"^- Status:\s*(.+?)\s*$", re.MULTILINE)
PROPOSAL_STATE_PATTERN = re.compile(r"^- Proposal state:\s*(.+?)\s*$", re.MULTILINE)
GENERATED_TIMESTAMP_PATTERN = re.compile(
    r"_Last generated: .*?_\n\n",
    re.MULTILINE,
)
IGNORED_DIRTY_PATHS = {STATUS_LEDGER_PATH.as_posix()}


@dataclass(frozen=True)
class RepoConfig:
    repo_id: str
    root: Path
    main_branch: str = "main"


@dataclass(frozen=True)
class ManifestRecord:
    branch: str | None
    manifest_path: Path
    plan_path: Path | None
    completion_ledger: str | None
    status: str | None
    proposal_state: str | None


def default_root() -> Path:
    package_root = Path(__file__).resolve().parent.parent
    if (package_root / STATUS_LEDGER_PATH).exists():
        return package_root
    return package_root.parent


def guess_repo_id(path: Path) -> str:
    result = run_command(["git", "rev-parse", "--git-common-dir"], path)
    if result.returncode == 0:
        common_dir = result.stdout.strip()
        if common_dir:
            return Path(common_dir).resolve().parent.name
    return path.name


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit live workstream state.")
    parser.add_argument(
        "--root",
        type=Path,
        default=default_root(),
        help="Repo root that owns docs/live-workstream-status.md and plan manifests.",
    )
    parser.add_argument(
        "--repo",
        action="append",
        default=[],
        metavar="ID=PATH",
        help="Additional repo roots to audit. Defaults to the root repo only.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Audit live branch/worktree state.")
    audit_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON.",
    )

    sync_parser = subparsers.add_parser(
        "sync-index",
        help="Refresh the generated current-state section in docs/live-workstream-status.md.",
    )
    sync_mode = sync_parser.add_mutually_exclusive_group()
    sync_mode.add_argument(
        "--check",
        action="store_true",
        help="Fail if the generated section is out of sync.",
    )
    sync_mode.add_argument(
        "--confirm",
        action="store_true",
        help="Write the generated section back to docs/live-workstream-status.md.",
    )

    return parser.parse_args()


def run_command(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def require_ok(result: subprocess.CompletedProcess[str], description: str) -> str:
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        raise RuntimeError(f"{description}: {detail}")
    return result.stdout


def parse_repo_specs(root: Path, raw_specs: list[str]) -> list[RepoConfig]:
    if raw_specs:
        repos = []
        for spec in raw_specs:
            if "=" not in spec:
                raise ValueError(f"invalid repo spec '{spec}', expected ID=PATH")
            repo_id, path = spec.split("=", 1)
            repos.append(RepoConfig(repo_id=repo_id.strip(), root=Path(path).resolve()))
        return repos

    root = root.resolve()
    return [RepoConfig(repo_id=guess_repo_id(root), root=root)]


def manifest_plan_path(manifest_path: Path) -> Path | None:
    if manifest_path.name.endswith(".plan.toml"):
        candidate = manifest_path.with_name(manifest_path.name.replace(".plan.toml", ".md"))
        if candidate.exists():
            return candidate
    return None


def parse_plan_value(path: Path | None, pattern: re.Pattern[str]) -> str | None:
    if path is None or not path.exists():
        return None
    match = pattern.search(path.read_text(encoding="utf-8"))
    if match is None:
        return None
    return match.group(1).strip().lower()


def parse_plan_status(path: Path | None) -> str | None:
    return parse_plan_value(path, STATUS_PATTERN)


def parse_plan_proposal_state(path: Path | None) -> str | None:
    return parse_plan_value(path, PROPOSAL_STATE_PATTERN)


def discover_manifests(root: Path) -> list[ManifestRecord]:
    manifests: list[ManifestRecord] = []
    plans_root = root / "docs" / "plans"
    if not plans_root.exists():
        return manifests
    for manifest_path in sorted(plans_root.rglob("*.plan.toml")):
        with manifest_path.open("rb") as handle:
            data = tomllib.load(handle)
        branch = data.get("branch")
        plan_path = manifest_plan_path(manifest_path)
        manifests.append(
            ManifestRecord(
                branch=str(branch) if branch else None,
                manifest_path=manifest_path.resolve(),
                plan_path=plan_path.resolve() if plan_path else None,
                completion_ledger=str(data.get("completion_ledger")) if data.get("completion_ledger") else None,
                status=parse_plan_status(plan_path),
                proposal_state=parse_plan_proposal_state(plan_path),
            )
        )
    return manifests


def git_worktrees(repo: RepoConfig) -> dict[str, dict[str, Any]]:
    output = require_ok(
        run_command(["git", "worktree", "list", "--porcelain"], repo.root),
        f"git worktree list failed for {repo.repo_id}",
    )
    entries: dict[str, dict[str, Any]] = {}
    for block in output.strip().split("\n\n"):
        if not block.strip():
            continue
        data: dict[str, Any] = {}
        for line in block.splitlines():
            key, value = line.split(" ", 1)
            data[key] = value
        branch_ref = data.get("branch")
        if not branch_ref:
            continue
        branch = str(branch_ref).removeprefix("refs/heads/")
        path = Path(str(data["worktree"])).resolve()
        status_output = require_ok(
            run_command(
                ["git", "-C", str(path), "status", "--short", "--branch", "--untracked-files=all"],
                repo.root,
            ),
            f"git status failed for worktree {path}",
        )
        status_lines = status_output.splitlines()
        dirty_entries = []
        for line in status_lines[1:]:
            candidate = line[3:] if len(line) > 3 else line
            if candidate in IGNORED_DIRTY_PATHS:
                continue
            dirty_entries.append(line)
        entries[branch] = {
            "path": str(path),
            "dirty": bool(dirty_entries),
            "dirty_entries": dirty_entries,
        }
    return entries


def git_branches(repo: RepoConfig) -> list[dict[str, Any]]:
    worktrees = git_worktrees(repo)
    output = require_ok(
        run_command(
            [
                "git",
                "for-each-ref",
                "refs/heads",
                "--format=%(refname:short)\t%(objectname)\t%(upstream:short)",
            ],
            repo.root,
        ),
        f"git for-each-ref failed for {repo.repo_id}",
    )

    branches: list[dict[str, Any]] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        branch, head, upstream = line.split("\t")
        merged = True
        if branch != repo.main_branch:
            merged_result = run_command(
                ["git", "merge-base", "--is-ancestor", branch, repo.main_branch],
                repo.root,
            )
            merged = merged_result.returncode == 0
        counts = require_ok(
            run_command(
                ["git", "rev-list", "--left-right", "--count", f"{repo.main_branch}...{branch}"],
                repo.root,
            ),
            f"git rev-list failed for {repo.repo_id}:{branch}",
        ).strip()
        behind, ahead = (int(part) for part in counts.split())
        worktree = worktrees.get(branch)
        branches.append(
            {
                "branch": branch,
                "head": head,
                "upstream": upstream or None,
                "merged_into_main": merged,
                "ahead_of_main": ahead,
                "behind_main": behind,
                "worktree": worktree,
            }
        )
    return branches


def classify_branch(
    branch: str,
    repo: RepoConfig,
    merged_into_main: bool,
    manifest_status: str | None,
    manifest_paths: list[str],
) -> str:
    if branch == repo.main_branch:
        return "main"
    if manifest_status == "promotion_ready":
        return "promotable"
    if manifest_status in {"active", "blocked"}:
        return "active"
    if manifest_status in {"promoted", "archived"}:
        return "historical"
    if branch.startswith(HISTORICAL_PREFIXES) or branch in HISTORICAL_NAMES:
        return "historical"
    if merged_into_main:
        return "merged_stale"
    if manifest_paths:
        return "active"
    return "diverged"


def build_audit(root: Path, repos: list[RepoConfig]) -> dict[str, Any]:
    manifests = discover_manifests(root)
    manifests_by_branch: dict[str, list[ManifestRecord]] = {}
    for manifest in manifests:
        if manifest.branch:
            manifests_by_branch.setdefault(manifest.branch, []).append(manifest)

    repo_payloads: list[dict[str, Any]] = []
    all_branch_names: set[str] = set()

    for repo in repos:
        branch_records = []
        dirty_worktrees = 0
        for branch_info in git_branches(repo):
            branch = str(branch_info["branch"])
            all_branch_names.add(branch)
            manifest_records = manifests_by_branch.get(branch, [])
            manifest_status = next((record.status for record in manifest_records if record.status), None)
            classification = classify_branch(
                branch=branch,
                repo=repo,
                merged_into_main=bool(branch_info["merged_into_main"]),
                manifest_status=manifest_status,
                manifest_paths=[str(record.manifest_path) for record in manifest_records],
            )
            worktree = branch_info["worktree"]
            if worktree and worktree["dirty"]:
                dirty_worktrees += 1
            branch_records.append(
                {
                    "branch": branch,
                    "head": branch_info["head"],
                    "upstream": branch_info["upstream"],
                    "classification": classification,
                    "merged_into_main": branch_info["merged_into_main"],
                    "ahead_of_main": branch_info["ahead_of_main"],
                    "behind_main": branch_info["behind_main"],
                    "worktree_path": worktree["path"] if worktree else None,
                    "dirty": worktree["dirty"] if worktree else False,
                    "dirty_entries": worktree["dirty_entries"] if worktree else [],
                    "manifest_paths": [str(record.manifest_path) for record in manifest_records],
                    "plan_paths": [str(record.plan_path) for record in manifest_records if record.plan_path],
                    "plan_status": manifest_status,
                    "proposal_state": next(
                        (record.proposal_state for record in manifest_records if record.proposal_state),
                        None,
                    ),
                }
            )

        repo_payloads.append(
            {
                "id": repo.repo_id,
                "root": str(repo.root),
                "main_branch": repo.main_branch,
                "branches": sorted(branch_records, key=lambda item: item["branch"]),
                "counts": {
                    "branches": len(branch_records),
                    "non_main_branches": sum(1 for item in branch_records if item["branch"] != repo.main_branch),
                    "attached_worktrees": sum(1 for item in branch_records if item["worktree_path"]),
                    "dirty_worktrees": dirty_worktrees,
                },
            }
        )

    pending_proposals = []
    branchless_plan_manifests = []
    for manifest in manifests:
        if not manifest.branch:
            continue
        if manifest.branch in all_branch_names:
            continue
        status = manifest.status or "unknown"
        proposal_state = manifest.proposal_state or "none"
        record = {
            "branch": manifest.branch,
            "classification": (
                "pending_proposal"
                if proposal_state == "pending"
                else "historical"
                if status in {"promoted", "archived"}
                else "branchless_plan"
            ),
            "status": status,
            "proposal_state": proposal_state,
            "manifest_path": str(manifest.manifest_path),
            "plan_path": str(manifest.plan_path) if manifest.plan_path else None,
        }
        if record["classification"] == "pending_proposal":
            pending_proposals.append(record)
        else:
            branchless_plan_manifests.append(record)

    branchless_plan_manifests = sorted(
        branchless_plan_manifests, key=lambda item: item["branch"]
    )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "repos": repo_payloads,
        "pending_proposals": sorted(pending_proposals, key=lambda item: item["branch"]),
        "branchless_plan_manifests": branchless_plan_manifests,
        # Keep the legacy key during the rename so older tooling does not break.
        "orphaned_manifests": branchless_plan_manifests,
    }


def short_path(path: str | None) -> str:
    if not path:
        return "-"
    return Path(path).name


def markdown_link(path: str | None) -> str:
    if not path:
        return "-"
    target = Path(path)
    return f"[{target.name}]({target})"


def preferred_plan_path(branch: str, plan_paths: list[str]) -> str | None:
    if not plan_paths:
        return None
    branch_slug = branch.split("/", 1)[-1]
    for path in plan_paths:
        if branch_slug in Path(path).name:
            return path
    return plan_paths[0]


def build_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def render_generated_section(payload: dict[str, Any]) -> str:
    lines = [
        GENERATED_START,
        "## Generated Status Snapshot",
        "",
        "This section is generated from live git and worktree state by the agent-systems workstream script.",
        "",
        f"_Last generated: {payload['generated_at']}_",
        "",
    ]

    summary_rows = []
    active_rows = []
    historical_rows = []
    for repo in payload["repos"]:
        counts = repo["counts"]
        summary_rows.append(
            [
                repo["id"],
                repo["main_branch"],
                str(counts["non_main_branches"]),
                str(counts["attached_worktrees"]),
                str(counts["dirty_worktrees"]),
            ]
        )
        for branch in repo["branches"]:
            if branch["branch"] == repo["main_branch"]:
                continue
            countless_classes = {"active", "promotable", "historical", "merged_stale"}
            row = [
                repo["id"],
                branch["branch"],
                branch["classification"],
                short_path(branch["worktree_path"]),
                "dirty" if branch["dirty"] else "clean",
                "-" if branch["classification"] in countless_classes else str(branch["ahead_of_main"]),
                "-" if branch["classification"] in countless_classes else str(branch["behind_main"]),
                markdown_link(preferred_plan_path(branch["branch"], branch["plan_paths"])),
            ]
            if branch["classification"] in {"active", "promotable", "diverged"}:
                active_rows.append(row)
            else:
                historical_rows.append(row)

    lines.append("### Summary")
    lines.extend(build_table(["Repo", "Main", "Non-main branches", "Attached worktrees", "Dirty worktrees"], summary_rows))
    lines.append("")

    lines.append("### Active, Promotable, And Diverged Branches")
    if active_rows:
        lines.extend(
            build_table(
                ["Repo", "Branch", "Class", "Worktree", "State", "Ahead", "Behind", "Plan"],
                active_rows,
            )
        )
    else:
        lines.append("None.")
    lines.append("")

    lines.append("### Historical And Merged-Stale Branches")
    if historical_rows:
        lines.extend(
            build_table(
                ["Repo", "Branch", "Class", "Worktree", "State", "Ahead", "Behind", "Plan"],
                historical_rows,
            )
        )
    else:
        lines.append("None.")
    lines.append("")

    lines.append("### Pending Proposals Without Live Branches")
    pending_proposals = payload["pending_proposals"]
    if pending_proposals:
        pending_rows = [
            [
                item["branch"],
                item["classification"],
                item["status"],
                item["proposal_state"],
                markdown_link(item["plan_path"] or item["manifest_path"]),
            ]
            for item in pending_proposals
        ]
        lines.extend(
            build_table(
                ["Branch", "Class", "Status", "Proposal State", "Plan"],
                pending_rows,
            )
        )
    else:
        lines.append("None.")
    lines.append("")

    lines.append("### Branchless Plan Manifests")
    branchless = payload["branchless_plan_manifests"]
    if branchless:
        branchless_rows = [
            [
                item["branch"],
                item["classification"],
                item["status"],
                item["proposal_state"],
                markdown_link(item["plan_path"] or item["manifest_path"]),
            ]
            for item in branchless
        ]
        lines.extend(
            build_table(
                ["Branch", "Class", "Status", "Proposal State", "Plan"],
                branchless_rows,
            )
        )
    else:
        lines.append("None.")
    lines.append(GENERATED_END)
    return "\n".join(lines)


def sync_index(root: Path, payload: dict[str, Any], check: bool, confirm: bool) -> int:
    ledger_path = root / STATUS_LEDGER_PATH
    content = ledger_path.read_text(encoding="utf-8")
    start = content.find(GENERATED_START)
    end = content.find(GENERATED_END)
    if start == -1 or end == -1 or end < start:
        raise RuntimeError(
            f"{ledger_path} is missing the generated workstream state markers"
        )
    end += len(GENERATED_END)
    rendered = render_generated_section(payload)
    updated = content[:start] + rendered + content[end:]
    if check:
        normalized_content = GENERATED_TIMESTAMP_PATTERN.sub("", content)
        normalized_updated = GENERATED_TIMESTAMP_PATTERN.sub("", updated)
        if normalized_content == normalized_updated:
            return 0
        print(f"{ledger_path} is out of sync with live workstream state", file=sys.stderr)
        return 1
    if confirm:
        ledger_path.write_text(updated, encoding="utf-8")
        print(f"updated {ledger_path}")
        return 0
    print(rendered)
    return 0


def emit_text(payload: dict[str, Any]) -> int:
    print(f"generated_at: {payload['generated_at']}")
    for repo in payload["repos"]:
        counts = repo["counts"]
        print(
            f"{repo['id']}: {counts['non_main_branches']} non-main branches, "
            f"{counts['attached_worktrees']} attached worktrees, "
            f"{counts['dirty_worktrees']} dirty"
        )
        for branch in repo["branches"]:
            if branch["branch"] == repo["main_branch"]:
                continue
            state = "dirty" if branch["dirty"] else "clean"
            worktree = branch["worktree_path"] or "-"
            print(
                f"  - {branch['branch']} [{branch['classification']}] "
                f"ahead={branch['ahead_of_main']} behind={branch['behind_main']} "
                f"{state} {worktree}"
            )
    if payload["pending_proposals"]:
        print("pending proposals:")
        for item in payload["pending_proposals"]:
            print(f"  - {item['branch']} [{item['classification']}] {item['plan_path'] or item['manifest_path']}")
    if payload["branchless_plan_manifests"]:
        print("branchless plan manifests:")
        for item in payload["branchless_plan_manifests"]:
            print(f"  - {item['branch']} [{item['classification']}] {item['plan_path'] or item['manifest_path']}")
    return 0


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    repos = parse_repo_specs(root, args.repo)
    payload = build_audit(root, repos)
    if args.command == "audit":
        if args.json:
            print(json.dumps(payload, indent=2))
            return 0
        return emit_text(payload)
    if args.command == "sync-index":
        return sync_index(root, payload, check=args.check, confirm=args.confirm)
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    sys.exit(main())
