# Assistant Adoption Prompt

Copy and paste this prompt into a coding assistant when you want it to adopt or
refresh this package in another repo.

```text
You are integrating the reusable `{{VENDOR_DIR}}/` package into this repo.

Work in the repo directly and make the changes yourself. Do not stop at advice.

Requirements:

1. Inspect the repo first and respect its existing structure, docs style, and
   test conventions.
2. Vendor or refresh `{{VENDOR_DIR}}/` from the canonical package if needed.
3. Create or update `{{CONFIG_FILE}}` for this repo.
   - Primary repo id: `{{REPO_ID}}`
   - Primary branch: `{{MAIN_BRANCH}}`
   - If linked repos are obvious from local context, record them.
   - If linked repos are ambiguous, do not invent them; leave the config rooted
     to the main repo only and call out the gap.
4. Point live instruction surfaces such as `AGENTS.md`, `CLAUDE.md`, or the
   repo's equivalent assistant entrypoints at
   `{{VENDOR_DIR}}/substantive-work-protocol.md`.
5. Add or refresh the repo-local planning surfaces expected by the package:
   - `docs/plans/README.md`
   - `docs/plans/plans-index.md`
   - `docs/live-workstream-status.md`
   - `docs/proposals/README.md` if the repo keeps proposal logs
   - `docs/adr/pending/README.md` if the repo keeps pending ADRs
6. Do not duplicate the canonical protocol docs outside `{{VENDOR_DIR}}/`.
   Repo-local docs should point back to the vendored package instead.
7. If the change is substantive, follow `{{VENDOR_DIR}}/substantive-work-protocol.md`:
   create a durable plan family, keep phases gated, and do not claim completion
   without the checker passing.
8. Run the narrowest validation needed for the repo plus the package checks that
   apply:
   - `python3 {{VENDOR_DIR}}/scripts/check_gated_plan.py ...`
   - `python3 {{VENDOR_DIR}}/scripts/workstream.py sync-index --confirm`
   - `python3 -m py_compile {{VENDOR_DIR}}/scripts/check_gated_plan.py {{VENDOR_DIR}}/scripts/workstream.py {{VENDOR_DIR}}/scripts/install.py`
9. Summarize:
   - what changed
   - what was verified
   - any linked repos or assistant entrypoints that still need human input

Keep the repo-specific overlay thin. If you discover a generic improvement to
`{{VENDOR_DIR}}/`, note that it should be upstreamed rather than kept as a
consumer-only fork.
```
