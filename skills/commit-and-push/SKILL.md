---
name: commit-and-push
description: Use when the user asks to commit, push, commit-and-push, open/draft a PR/MR, or write a PR description with a Test plan — especially when changes should be split into logical commits, or when tempted to dump everything into one commit or push to a protected branch.
---

# Commit and Push

## Overview

**Commit in reviewable batches, push the feature branch, sync the MR/PR (create after asking, update automatically) with a Test plan.**

Path: inspect → batch → commit → push → draft MR/PR copy → sync MR/PR (detect → update or ask-to-create) → report.
Does **not** replace test-design judgment (see test-design) or TDD rhythm (see superpowers:test-driven-development).

**Core principle: one commit = one reviewable intent with a Conventional-Compliant, non-obscured message; one PR = one shippable story with a falsifiable Test plan.**

**Core rules on copy:** commit/PR message format is a hard gate — Conventional Commits, `type(scope): subject`, type from the standard enum, scope from repo convention; **language is flexible** (中文 / English), following the user's own phrasing/register, not translated into an alien voice.

## When to Use

- User says commit / push / "commit and push" / draft or open a PR/MR
- Working tree mixes concerns that should not land in one commit
- Need a PR Summary + **Test plan** checklist

**When NOT to use:** review-only with no ship intent; only designing tests (use test-design). (If a transition gate upstream offered a review and the user declined, proceed on their call.)

## The Iron Law (non-negotiable)

```
1. NEVER commit or push to a protected branch (default: main, master, pro, test — plus any the repo declares).
2. NEVER mix unrelated intents in one commit.
3. EVERY PR/MR description MUST include an actionable "## Test plan" checklist.
4. EVERY commit message MUST be Conventional-Compliant (`type(scope): subject`) and non-obscured (below); language is free (中文/English) but the format is not.
5. NEVER create a NEW MR/PR without an explicit yes; ALWAYS update an EXISTING one for this branch (automatic, full rewrite).
```

**Violating the letter is violating the spirit.** "Just one quick commit on test", "I'll add the Test plan later", and "force push is fine this once" do not count.

## Workflow (when invoked)

Announce "Using commit-and-push to …", then **create one todo per step**:

1. **Confirm workspace + branch + upstream** (§0) — stop if protected.
2. **Inspect and plan batches** (§1) — show the plan; execute by default unless ownership is unclear.
3. **Sample the user's voice** (§1.5) — from this feature's conversation, not git history.
4. **Commit each batch** (§2) — stage only that batch; message answers *why*, Conventional + non-obscured.
5. **Push the feature branch** (§3) — never force to protected branches; ask before any force.
6. **Draft MR/PR title + description with Test plan** (§4) — from *all* commits vs baseline, not only HEAD.
7. **Sync the MR/PR** (§4.5) — detect an existing MR/PR for this branch; if one exists, **update it automatically** (full rewrite); if none, **ask** before creating.
8. **Report** (§5) — paths, commits, push result, MR/PR number + URL, leftovers.

Do **not** create a new MR/PR without an explicit yes (§4.5); updating an existing one is automatic.

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

## §1.5 Sample the user's voice (before writing any copy)

Before drafting commit messages or PR copy, **listen to how the user talks about this change** — their register, not the repo's history.

**Source priority (do not invert):**

1. **This conversation, this feature's whole lifetime** — every round where they described the work, corrected the wording, or set the direction (not just the last turn). Short, direct, says the outcome; concrete nouns and verbs.
2. **Cross-session memory file** (if one exists) — a settled register from prior work on this repo.
3. **Fallback: the hard rules below** — only when neither exists (e.g. user just said "commit this").

**Why not `git log --author`:** in AI-collaborator repos the history is mostly AI-written long clauses (e.g. this repo's `fix(skills): make skill copy English-only Translate…`); sampling it trains the obscurity right back in.

**What "like the user" means — and what it does NOT:**
- It does **not** mean inventing a persona; with no signal, stay neutral and stable (rule 3).
- It does **not** override hard rules — the Conventional format and the non-obscuring checklist below beat any sampled phrasing.

### Non-obscuring checklist (hard, applies to every message)

- Subject ≤ ~50 chars of substance; one line
- Start the summary with the **outcome/result verb** (add, ship, route, expose, fix, drop…), not an adjective stack
- No piled modifiers; no vague verbs ("improve", "better", "make nicer"); no file-name dump
- `type` = primary user-visible intent (don't stack every type)
- Match the repo's recent commit style (language included — 中文 or English as the user writes)

## §2 Commit each batch

Re-check: branch and upstream are not protected. Else **STOP**.

For each batch, in order:

1. `git add` **only** that batch's files
2. `git diff --cached` to verify
3. Write the message (Conventional Commits, **hard gate** — `type(scope): subject`, type from the standard enum, scope from repo convention):
   - Subject: one line, ≤ ~50 chars, outcome verb first, language as the user writes (中文 or English — no forced translation)
   - Body (optional): 1–2 sentences on **why / outcome**, not a file dump
   - Run the non-obscuring checklist from §1.5 before committing
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

Chinese example — same shape, user's own language:

```bash
git commit -m "feat(scope): 导出前新增类型校验，防止空值落库"
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

- One line, `type(scope): summary` — **Conventional, hard gate** (type from standard enum, scope from repo convention)
- `type` = primary user-visible intent (don't stack every type)
- Summary = **why / outcome**, ≤ ~50 chars of substance, outcome verb first, no stacked modifiers
- Language as the user writes (中文 / English) — use the §1.5 voice sample

### Description template (always)

```markdown
## Summary
- <1–3 bullets covering ALL commits in this PR and the motivation>
- <optional: key tradeoff>

## Test plan

### Automated (ran before commit)
- [x] <command/check already executed before this commit — evidence, not a to-do>
- [x] <another command that actually ran>

### Acceptance (user/product)
- [ ] <manual step for a human/PM to verify — what they should see/feel>
- [ ] <another scenario to demo>
```

**Test plan rules:**

- Checklist items must be **doable** by a reviewer (command, URL, scenario) — not "run the tests" with no target
- **Two blocks, one intent:** `Automated (ran before commit)` lists scripts that **actually ran** (checked, with the command); `Acceptance (user/product)` lists open manual steps for a human to verify — what they should see/feel
- **Honesty rule:** nothing goes in the Automated block unless it was actually run before commit. A check that didn't run either stays unmarked or moves to Acceptance as "待验证 / to verify"
- Map items to real risks in *this* diff (routing, config, compatibility, prompts, migrations, …)
- Prefer behavior checks over "coverage went up"

**Do not** create a new MR/PR without an explicit yes — see §4.5.
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

### Automated (ran before commit)
- [x] ...

### Acceptance (user/product)
- [ ] ...
```

## §4.5 Sync the MR/PR (detect → update or ask-to-create)

Detect whether an MR/PR already exists for **this branch on origin**. Result drives the action:

1. **Detect** the host from `git remote get-url origin` (GitHub → `gh`, GitLab → `glab`; unknown host → skip to paste-ready copy only).
2. **Check for an existing MR/PR for the current branch**:

   ```bash
   # GitHub
   gh pr list --head "$(git branch --show-current)" --state open --json number,title,url --jq '.[0]'
   # GitLab
   glab mr list --source-branch "$(git branch --show-current)" --state open --output json | head -c 1000
   ```

3. **Existing MR/PR found → UPDATE it automatically** (no question; the user asked for automatic updates). Regenerate title + description from `baseline..HEAD` (§4), then:

   ```bash
   # GitHub
   gh pr edit <NUMBER> --title "<title>" --body-file /tmp/pr-body.md
   # GitLab
   glab mr update <NUMBER> --title "<title>" --description "$(cat /tmp/pr-body.md)"
   ```

   Write the body to a temp file first (readable + reproducible), then edit. Say what was updated (#N + title).

4. **No MR/PR found → ask before creating** (one AskUserQuestion; creating requires an explicit yes):

   ```
   A) Recommended: Create the MR/PR now (title + body with Test plan from §4)
   B) Don't create — just keep the paste-ready copy
   C) Something else (I will type it)
   ```

   Only on **A** create it:

   ```bash
   # GitHub
   gh pr create --base <baseline-branch> --head "$(git branch --show-current)" \
     --title "<title>" --body-file /tmp/pr-body.md
   # GitLab
   glab mr create --source-branch "$(git branch --show-current)" \
     --target-branch <baseline-branch> --title "<title>" --description "$(cat /tmp/pr-body.md)"
   ```

   On **B**, include the paste-ready copy in the report and stop.

**Update semantics:** full rewrite of title + body from `baseline..HEAD` every time — the description always reflects all current commits, Test plan included. Manual edits to a previously-created MR/PR description are overwritten (per decision).

## §5 Final report

1. Workspace path, worktree?, branch, upstream  
2. Commit list (hash + message)  
3. Push result (remote branch, upstream set?)  
4. MR/PR: detected #N + URL and whether it was **updated automatically** / **created (on user's yes)** / **copy only (user declined)** — with title + description  
5. Leftover unstaged/uncommitted files and why  
6. One-line next step

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
| "English-only commits are the only right way" | Format is hard; language is free. Match the user's register (中文/English). |
| "Use git history for the user's voice" | History is mostly AI-written. Sample the live conversation instead. |
| "Include the .env so it works on CI" | Secrets never get committed. Warn and skip. |
| "MR/PR already exists — skip the sync" | Existing MR/PR gets updated automatically every push; a stale description is a wrong claim. |
| "Just create the MR/PR, no need to ask" | Creation is irreversible on a shared host — ask first (§4.5). |

## Red Flags — stop immediately

- About to commit/push on `main` / `master` / `pro` / `test` (or repo-protected equivalents)
- Staging unrelated features/fixes/docs in one commit "to be done"
- PR body with no `## Test plan` or only vague "test it"
- Automated block that claims a script ran when it did not
- Using `--force` / `--no-verify` without an explicit user request
- Creating a **new** MR/PR without an explicit yes (§4.5)
- Skipping the existence check and leaving a stale MR/PR description after a push
- Commit message that only lists file names

**Any hit → stop, return to the Iron Law.**

## Checklist

- [ ] Not on a protected branch; upstream not protected
- [ ] Batches are single-intent; plan shown
- [ ] Each commit message is Conventional-Compliant + non-obscured (§1.5); language follows user's register; no secrets staged
- [ ] Pushed to `origin <feature-branch>` only
- [ ] PR title + Summary cover **all** commits vs baseline
- [ ] `## Test plan` has Automated (ran, checked) + Acceptance (open manual) blocks, both concrete
- [ ] MR/PR checked for this branch: existing → updated automatically; none → asked before creating (or user declined)
