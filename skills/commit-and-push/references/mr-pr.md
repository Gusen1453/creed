# MR/PR description and sync (host side)

Sections §4–§4.5 of **commit-and-push**: draft the title + description for the right *intent*, then detect/create/update the MR/PR. The commit/push side is [commit.md](commit.md); raw CLI traps are [host-cli.md](host-cli.md).

## §4 Draft MR/PR title and description (required)

Base the copy on **all commits since the integration baseline**, not only the latest commit.

### Baseline

The baseline is **the base branch of the MR/PR you are about to sync — not a hardcoded branch**. Picking the wrong baseline silently produces an empty or wrong description.

1. If an MR/PR already exists for this branch, use its **target base** as the baseline (§4.5 detects it): `baseline = origin/<target_branch>`.
2. No MR/PR yet → use **the repo's integration branch** (whatever plays that role — `test`, `dev`, `staging`, `develop`, …), else the default branch (`origin/main` / `origin/master`, or `git symbolic-ref refs/remotes/origin/HEAD`).

State which baseline you used and why. **Sanity-check it:** `baseline..HEAD` must be non-empty; an empty list on a branch you know has commits means you picked the wrong base (e.g. a promotion MR whose source *is* the integration branch has `<integration>..HEAD` = 0; the right base is the production branch).

```bash
git fetch origin 2>/dev/null || true
git log --oneline origin/<base>..HEAD
git diff --stat origin/<base>...HEAD
```

**Counts must come from `git rev-list --count` (merges included)** — that is GitLab/GitHub's commit-count convention; `--no-merges` undercounts and will not match the host's number.

### Pick the intent, then the template

The description's emphasis depends on **what the MR is for** — a verifier's verification handoff, a release promotion, and an on-call incident hotfix are different documents. Branch names are a **hint, not the rule**: infer the *intent* from source → target plus the repo's naming, and fall back to the generic template when it's unclear.

| Intent (what the MR is doing) | Kind | Template | Emphasis |
|---|---|---|---|
| **Change → independent verification** — a feature/fix awaiting someone else's sign-off, into an integration / QA / staging / dev branch | verification handoff | [feature-to-integration.md](../assets/feature-to-integration.md) | impact surface + how-to-verify + known limits |
| **Promotion → production** — an already-verified line of work shipping into prod | release promotion | [integration-to-production.md](../assets/integration-to-production.md) | release notes by feature + risky surfaces + deploy order + rollback |
| **Fix → production now** — an out-of-band fix that skips the verification stage | incident hotfix | [hotfix-to-production.md](../assets/hotfix-to-production.md) | root cause + rollback + the repro that proves it |
| none of the above (e.g. a docs/chore branch, or intent unclear) | generic | the inline template below | summary + Test plan |

**Do not match on branch names literally.** The production branch may be `main`, `master`, `pro`, `prod`, `release`, `production`, …; the integration branch may be `test`, `dev`, `staging`, `qa`, `develop`, …. Decide **which branch plays which role** in *this* repo first (from its naming, README, or the MR's own `target_branch`), then pick the intent:

- source is a feature/fix branch, target is the **non-production integration** role → verification handoff
- source is the **integration** role, target is the **production** role → release promotion
- source is a fix, target is the **production** role, and it bypasses integration → incident hotfix
- otherwise → generic

Detect once per MR (§4.5 already has `source`/`target`); if the roles are ambiguous, use the generic template and say why. **Every template inherits the hard rules below** (Conventional title, honesty rule on `Automated`, no secret/env values). The release/hotfix templates replace the generic `## Test plan` with their own verification section — allowed; the `Automated` honesty rule still applies.

### Title

- One line, `type(scope): summary` — **Conventional, hard gate** (type from standard enum, scope from repo convention)
- `type` = primary user-visible intent (don't stack every type)
- Summary = **why / outcome**, ≤ ~50 chars of substance, outcome verb first, no stacked modifiers
- Language as the user writes (Chinese / English) — the [voice.md](voice.md) chain (MR inherits register from its commits, not directly from the query)
- **Release/hotfix flows** may instead name the release/symptom (`release(vX.Y.Z): …` / `fix(scope): <symptom>`), per their template

### Description template — generic fallback

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
- **Honesty rule:** nothing goes in the Automated block unless it was actually run before commit. A check that didn't run either stays unmarked or moves to Acceptance as "to verify / to verify"
- Map items to real risks in *this* diff (routing, config, compatibility, prompts, migrations, …)
- Prefer behavior checks over "coverage went up"

### Issue linkage (closing keyword)

When the work came from a filed issue, add a closing keyword so the issue closes itself on merge.

- **Preferred source: the number this session already has** — if the issue was filed (or read) in this conversation, use that `<N>`.
- **Fallback: the branch name**, matching either `#<N>` anywhere or a leading `<N>-` (the shape the `issue` skill suggests is `123-fix-export-empty-row`, **no `#`** — a `#`-only matcher would never fire).
- **Neither present → do not guess.** Say the linkage could not be determined rather than inventing a number.

Write it in the description (both hosts accept `Closes #<N>`; GitLab also accepts `Closes #<N>` and treats it the same).

**Do not** create a new MR/PR without an explicit yes — see §4.5.
If the remote prints a "create merge request" URL after push, include it in the report.

### Paste-ready output

**Title**

```
<one-line title>
```

**Description**

Use the matching template from [assets/](../assets/) (or the generic template above), filled in — never a bare title with no body.

## §4.5 Sync the MR/PR (detect → update or ask-to-create)

Detect whether an MR/PR already exists for **this branch on origin**. Result drives the action:

1. **Detect** the host by asking each CLI to resolve `origin` — `gh repo view` exits 0 → GitHub, `glab repo view` exits 0 → GitLab, neither → unknown host (skip to paste-ready copy only). Do not judge by the hostname's spelling (self-hosted GitLab rarely says "gitlab"), and not by `glab api version` (it ignores `origin`) ([host-cli.md](host-cli.md) §Detect host).
2. **List MR/PRs for the current branch — including merged/closed** (default lists only open; a merged MR must still be visible or you will wrongly offer to create a duplicate):

   ```bash
   BR="$(git branch --show-current)"
   # GitHub — newest PR (any state) from this head branch
   gh pr list --head "$BR" --state all --json number,title,url,state,baseRefName \
     --jq 'sort_by(.number)|last'
   # GitLab — -A is REQUIRED (default hides merged/closed); --state is NOT a valid flag.
   # A source branch can map to several MRs over time → filter by target_branch, take newest iid.
   glab mr list -A --source-branch "$BR" -F json \
     --jq 'sort_by(.iid)|last'
   #   or, when you know the target role:  --jq '[.[]|select(.target_branch=="<prod-branch>")]|sort_by(.iid)|last'
   ```

   `glab mr list --state open` is a **hard error** (`Unknown flag: --state`). If several target branches exist, prefer the one whose `target_branch` plays the production/integration role this branch merges into.

   **Prefer `mr list --source-branch` over `mr view <branch>`** — `glab mr view` accepts a branch name only when it resolves to a single MR; on a long-lived branch (many historical MRs, none currently open) it fails with `You must select a merge request: merge request ID number required`. `mr list --source-branch` + `-A` is the reliable branch lookup.

3. **MR/PR found → UPDATE it automatically** (no question — the user asked for automatic sync). Determine **state** first:

   - **opened** → update the title/body (below).
   - **merged/closed** → do **not** offer to create a new one silently; report it and ask (a merged MR means the branch already shipped — a new MR is usually a mistake).

   Regenerate the description from `baseline..HEAD` (§4 — baseline = this MR's target base), write it to a temp file, then update:

   ```bash
   # GitHub
   gh pr edit <NUMBER> --title "<title>" --body-file "$BODY"
   # GitLab — the -d form is byte-exact (verified roundtrip); avoid glab api entirely
   glab mr update <NUMBER> --title "<title>" -d "$(cat "$BODY")"
   ```

   - GitLab: prefer `glab mr update <N> -d "$(cat body.md)"` — it roundtrips content byte-for-byte (backticks, `→`, `−` all safe). **Never** `-d -` (opens an editor; a non-interactive agent hangs).
   - If you must use `glab api` for something the CLI doesn't cover: use `--field`/`-F` (which expands `@file`), **never** `--raw-field`/`-f` (sends the literal string `@file` — silent data loss, exit 0). `--input <file>` needs an explicit `-H "Content-Type: application/json"` or it returns 415.

4. **No MR/PR found → ask before creating** (one AskUserQuestion; creating requires an explicit yes):

   ```
   A) Recommended: Create the MR/PR now (title + body with Test plan from §4)
   B) Don't create — just keep the paste-ready copy
   C) Something else (I will type it)
   ```

   Only on **A** create it:

   ```bash
   # GitHub
   gh pr create --base <target-branch> --head "$BR" --title "<title>" --body-file "$BODY"
   # GitLab
   glab mr create --source-branch "$BR" --target-branch <target-branch> \
     --title "<title>" -d "$(cat "$BODY")"
   ```

   On **B**, include the paste-ready copy in the report and stop.

5. **Read back after any write (mandatory).** `exit 0` is not evidence. Re-fetch and compare the stored description against `$BODY`; a mismatch means the write silently failed (e.g. the `-f @file` trap) — fix it, don't report success.

   ```bash
   # GitLab — diff surfaces the exact difference (host may normalize a trailing newline; that alone is fine)
   diff <(glab mr view <N> -F json | jq -r '.description') "$BODY"
   # GitHub
   diff <(gh pr view <N> --json body --jq .body) "$BODY"
   ```

**Update semantics — match the MR's kind, don't blindly rewrite:**

- **verification handoff (change → verification)** — short-lived: full rewrite of title + body from `baseline..HEAD`. Manual edits are overwritten.
- **release promotion (promotion → production)** — long-lived: **incremental re-derivation** — preserve the existing prose sections and hand-curated tables, recompute only stale numbers (commit/file counts), add a section for the new commits, append acceptance rows. **Never** regenerate from the commit list, which collapses a curated release note into a changelog.
- **incident hotfix (fix → production)** — one-shot: regenerate, terse, single commit.
- If unsure which kind, ask.

**Some content cannot be derived from git** — e.g. a commit-attribution table keyed by feature/author, an **`@handle` owner list**, or a hand-written release narrative. Never auto-generate these; carry them forward from the existing description or ask.

**Owner mentions (release / hotfix).** The owner is normally the git user who owns the change; use their host handle, and if it differs from `user.name` that is a point to **confirm with the user**, not to guess. If a ping must actually reach someone, set `--assignee`/`--reviewer` (or post a comment) rather than relying on a body mention — commands in [host-cli.md](host-cli.md).
