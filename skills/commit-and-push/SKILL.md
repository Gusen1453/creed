---
name: commit-and-push
description: Use when the user asks to commit, push, commit-and-push, open/draft a PR/MR, or write a PR description with a Test plan — especially when changes should be split into logical commits, or when tempted to dump everything into one commit or push to a protected branch.
---

# Commit and Push

## Overview

**Commit in reviewable batches, push the feature branch, draft PR/MR copy with a Test plan.**

Path: inspect → batch → commit → push → draft PR title + description.
Does **not** replace test-design judgment (see test-design) or TDD rhythm (see superpowers:test-driven-development).

**Core principle: one commit = one reviewable intent; one PR = one shippable story with a falsifiable Test plan.**

## When to Use

- User says commit / push / "commit and push" / draft or open a PR/MR
- Working tree mixes concerns that should not land in one commit
- Need a PR Summary + **Test plan** checklist

**When NOT to use:** review-only with no ship intent; only designing tests (use test-design).

## The Iron Law (non-negotiable)

```
1. NEVER commit or push to a protected branch (default: main, master, pro, test — plus any the repo declares).
2. NEVER mix unrelated intents in one commit.
3. EVERY PR/MR description MUST include an actionable "## Test plan" checklist.
```

**Violating the letter is violating the spirit.** "Just one quick commit on test", "I'll add the Test plan later", and "force push is fine this once" do not count.

## Workflow (when invoked)

Announce "Using commit-and-push to …", then **create one todo per step**:

1. **Confirm workspace + branch + upstream** (§0) — stop if protected.
2. **Inspect and plan batches** (§1) — show the plan; execute by default unless ownership is unclear.
3. **Commit each batch** (§2) — stage only that batch; message answers *why*.
4. **Push the feature branch** (§3) — never force to protected branches; ask before any force.
5. **Draft PR/MR title + description with Test plan** (§4) — from *all* commits vs baseline, not only HEAD.
6. **Report** (§5) — paths, commits, push result, paste-ready PR copy, leftovers.

Do **not** create the PR/MR via API/`gh pr create` unless the user explicitly asks to create it.

## §0 Confirm workspace, branch, upstream

Run in the **current workspace git root** (worktree or main checkout — both OK):

```bash
git rev-parse --show-toplevel
git branch --show-current
git branch -vv
git rev-parse --abbrev-ref @{upstream} 2>/dev/null || true
git worktree list
git status
git remote -v
```

**Protected if any of these hold → STOP** (no commit, no push):

- Current branch is protected (`main` / `master` / `pro` / `test`, or repo-documented equivalents)
- `@{upstream}` resolves to `origin/<protected>`
- Planned push target is `origin/<protected>`

If upstream wrongly tracks a protected branch: `git branch --unset-upstream` (or retarget to `origin/<feature>`) before continuing. **Never** push to the protected remote branch to "fix" it.

| Scenario | Action |
|----------|--------|
| Feature branch (`feat/*`, `fix/*`, `chore/*`, `docs/*`, …); upstream not protected | Proceed; push `origin HEAD` |
| Same, whether or not under `.worktrees/` | Proceed |
| On protected branch | **Stop**; create/switch to a feature branch first |
| Upstream is protected | **Stop** or fix upstream first |

Record for the final report: toplevel path, worktree?, branch, upstream, push target.

## §1 Inspect and plan batches

```bash
git status
git diff
git diff --cached
git log --oneline -10
```

Split by **logical units** (each batch: one intent, independently reviewable):

- Separate `feat` / `fix` / `refactor` / `test` / `docs` / `chore`
- Keep product code apart from pure tests/fixtures/recordings when the story differs
- Split unrelated subsystems
- Never smuggle drive-by cleanups into a feature commit

Briefly list the batch plan (files + proposed `type(scope)`). **Execute by default**; ask only when batch ownership is ambiguous.

## §2 Commit each batch

Re-check: branch and upstream are not protected. Else **STOP**.

For each batch, in order:

1. `git add` **only** that batch's files
2. `git diff --cached` to verify
3. Write the message (prefer Conventional Commits: `feat(scope): …`):
   - 1–2 sentences on **why / outcome**, not a file dump
   - Match the repo's recent commit style (language included)
4. Commit (no `--no-verify`, no `--no-gpg-sign`, no `git config` changes unless the user explicitly asks)

```bash
git commit -m "$(cat <<'EOF'
feat(scope): short statement of intent

Optional body for context reviewers need.
EOF
)"
```

PowerShell:

```powershell
git commit -m @"
feat(scope): short statement of intent

Optional body for context reviewers need.
"@
```

5. `git status`. If a hook fails: **fix and make a NEW commit**. Do not amend unless all amend-safety conditions hold (user asked, or hook auto-modified files after a commit *you* created in this conversation; HEAD not pushed).

Also:

- Skip secrets (`.env`, credentials, tokens); warn and leave them unstaged
- Never `reset --hard` / destructive git unless the user explicitly asks

## §3 Push the feature branch

```bash
git branch --show-current
git status
git log --oneline @{u}..HEAD 2>/dev/null || git log --oneline "origin/$(git branch --show-current)..HEAD" 2>/dev/null || true
```

- Protected branch or protected upstream → **STOP**
- Else: `git push -u origin HEAD`
- If remote moved: `git pull --rebase origin <branch>`, resolve, push again
- If force seems required: **ask the user first**. Never force-push to protected branches (`main`/`master`/`pro`/`test`/…).

## §4 Draft PR/MR title and description (required)

Base the copy on **all commits since the integration baseline**, not only the latest commit.

### Baseline

Default baseline: `origin/test` if it exists (common integration branch); else `origin/main` / `origin/master`. State which baseline you used.

```bash
git fetch origin 2>/dev/null || true
git log --oneline origin/test..HEAD   # or origin/main..HEAD
git diff --stat origin/test...HEAD
```

### Title

- One line, prefer `type(scope): summary`
- `type` = primary user-visible intent (don't stack every type)
- Summary = **why / outcome**, ~50 chars of substance

### Description template (always)

```markdown
## Summary
- <1–3 bullets covering ALL commits in this PR and the motivation>
- <optional: key tradeoff>

## Test plan
- [ ] <executable check tied to a real risk in this diff>
- [ ] <another concrete path: API, config, regression, docs link, …>
```

**Test plan rules:**

- Checklist items must be **doable** by a reviewer (command, URL, scenario) — not "run the tests" with no target
- Map items to real risks in *this* diff (routing, config, compatibility, prompts, migrations, …)
- Prefer behavior checks over "coverage went up"

**Do not** call `gh pr create` / GitLab APIs unless the user asks to create the PR/MR.
If the remote prints a "create merge request" URL after push, include it in the report.

### Paste-ready output

**Title**

```
<one-line title>
```

**Description**

```markdown
## Summary
...

## Test plan
...
```

## §5 Final report

1. Workspace path, worktree?, branch, upstream  
2. Commit list (hash + message)  
3. Push result (remote branch, upstream set?)  
4. PR title + description (required)  
5. Leftover unstaged/uncommitted files and why  
6. One-line next step (e.g. open MR into `test` and paste the copy) — do not create it yourself unless asked  

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "One big commit is faster" | Reviewers can't bisect or revert cleanly. Batch by intent. |
| "I'll push to test just this once" | Protected means protected. Feature branch + MR. |
| "Test plan later / obvious" | Without a checklist, 'done' is a claim. Always include `## Test plan`. |
| "Force push will clean the history" | Ask first. Never force protected branches. |
| "Hook is annoying — skip with --no-verify" | Fix the cause. Skipping hooks is not shipping. |
| "Amend the failed hook commit" | New commit after fix, unless amend-safety rules all hold. |
| "PR description = last commit message" | PR covers the whole `baseline..HEAD` story. |
| "Include the .env so it works on CI" | Secrets never get committed. Warn and skip. |

## Red Flags — stop immediately

- About to commit/push on `main` / `master` / `pro` / `test` (or repo-protected equivalents)
- Staging unrelated features/fixes/docs in one commit "to be done"
- PR body with no `## Test plan` or only vague "test it"
- Using `--force` / `--no-verify` without an explicit user request
- Creating a PR/MR via tooling when the user only asked for commit/push copy
- Commit message that only lists file names

**Any hit → stop, return to the Iron Law.**

## Checklist

- [ ] Not on a protected branch; upstream not protected
- [ ] Batches are single-intent; plan shown
- [ ] Each commit message states why; no secrets staged
- [ ] Pushed to `origin <feature-branch>` only
- [ ] PR title + Summary cover **all** commits vs baseline
- [ ] `## Test plan` has concrete, checkable items
- [ ] Did not auto-create PR/MR unless asked
