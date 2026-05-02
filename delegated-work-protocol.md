# Delegated Work Protocol

This protocol wraps delegated sandbox jobs for a repo that vendors
`agent-protocols/`.

Use it when a coding worker, research worker, or other sandboxed job may be
summarized back to the operator as done, ready for review, or complete.

## Required Quality Evidence

Before a delegated coding job starts, the runtime should record a preflight
report with:

- host project directory and delegated container working directory
- resolved git worktree root when available
- current branch and commit when git metadata is available
- recorded baseline branch or commit for implementation work
- effective worker mode, model, reasoning effort, and sandbox mode
- expected developer tools, starting with `git` and `rg`
- whether browser or mobile verification is required by the task
- whether the job may start cleanly, start degraded, or fail before execution

The preflight report is runtime evidence. Prompt text may point workers at this
protocol, but prompt text is not the enforcement mechanism.

## Completion Quality

Delegated jobs finish with one quality state:

- `passed`: preflight, worker execution, follow-ups, final git checkpoint, and
  required verification all produced sufficient evidence
- `degraded_preflight`: the job ran after a non-fatal environment issue
- `degraded_workers`: follow-up workers or resume launches failed
- `degraded_verification`: required browser or mobile verification evidence is
  missing or incomplete
- `failed_gate`: a required gate failed and the job should not be treated as
  complete

If more than one degraded state applies, the runtime reports the most severe
state and preserves all issues in the job quality log.

## Final Git Checkpoint

Any delegated job that mutates repo files and reports `passed`,
`ready_for_review`, `complete`, or an equivalent terminal state must finish
with a clean git checkpoint.

The final checkpoint requires:

- `git status --porcelain --untracked-files=all` is empty in the delegated
  worktree
- implementation work has `HEAD` ahead of the recorded baseline branch or
  commit
- the final job result records branch, commit, pushed: yes/no, and
  worktree_clean: true/false

A dirty worktree at final response time is `failed_gate`. Do not report dirty
implementation output as ready for review, and do not downgrade uncommitted
source, doc, schema, or config changes to a degraded completion.

Non-mutating exploratory jobs do not need a git checkpoint. If an exploratory
or proposal-only job creates durable repo artifacts, those artifacts must be
committed or explicitly discarded before the job can be reported as complete.

## Browser And Mobile Verification

Visual UI work must declare browser verification requirements. Mobile-sensitive
work must also require a narrow viewport check.

Evidence should record the route, viewport, browser/tool, target visibility,
and any captured artifact path when available. If verification cannot run, the
job may still finish, but it must finish as `degraded_verification`.

## Follow-Up Workers

Follow-up prompts, resume sessions, and spawned workers must report failures as
quality issues. A follow-up launch failure may leave the primary task output
usable, but the parent job quality must become `degraded_workers` unless the
failure makes the whole job fail.

## Escalation

Delegated work does not replace the substantive work protocol. Escalate to the
substantive protocol when the delegated task crosses ownership boundaries,
touches durable contracts, changes schema or public surfaces, requires multiple
reviewable slices, or needs gated phase evidence to be considered done.
