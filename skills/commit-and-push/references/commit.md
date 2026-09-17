# Commit and push (git side)

Sections §0–§3 of **commit-and-push**: confirm the workspace, split into batches, commit each batch, push the feature branch. The MR/PR side is [mr-pr.md](mr-pr.md); host CLI traps are [host-cli.md](host-cli.md).

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

## §1.5 Voice

Commit is the **nearest-to-the-query** layer of the copy chain — the commit message should read almost like the user's own request. The chain, the register source, and the hard checklist live in one place: **[voice.md](voice.md)**. Read it before writing any copy (commit, MR, tag, release).

## §2 Commit each batch

Re-check: branch and upstream are not protected. Else **STOP**.

For each batch, in order:

1. `git add` **only** that batch's files
2. `git diff --cached` to verify
3. Write the message (Conventional Commits, **hard gate** — `type(scope): subject`, type from the standard enum, scope from repo convention):
   - Subject: one line, ≤ ~50 chars, outcome verb first, language as the user writes (中文 or English — no forced translation)
   - Body (optional): 1–2 sentences on **why / outcome**, not a file dump
   - Run the non-obscuring checklist from [voice.md](voice.md) before committing
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

### Push auth fails in a non-interactive shell (real trap)

Symptom: `fatal: Cannot prompt because user interactivity has been disabled.` / `unable to get password from user`. The remote is HTTPS and git wants a credential the sandbox can't prompt for.

Fix once per machine:

```bash
gh auth setup-git      # wires gh's credential helper into git; HTTPS pushes then use the gh token
```

Then retry. (`gh` being logged in is not enough on its own — it must be the configured credential helper, and the remote must be HTTPS for this to apply. If you cannot fix it, ask the user to run `git push` themselves.)
