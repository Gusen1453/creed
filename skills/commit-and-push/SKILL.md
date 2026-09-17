---
name: commit-and-push
description: Use when the user asks to commit, push, commit-and-push, open/draft a PR/MR, write a PR description with a Test plan, or tag/cut a release — especially when changes should be split into logical commits, or when tempted to dump everything into one commit or push to a protected branch.
---

# Commit and Push

> **Output language:** answer and write artifacts in the user's own language (match their messages, not the repo's history).

## Overview

**Commit in reviewable batches, push the feature branch, sync the MR/PR (create after asking, update automatically) with an intent-appropriate description, and — when a release is called for — tag the shipped commit and publish the release.**

Each stage has its own reference — this file is a router:

| Stage | What | Reference |
|------|------|-----------|
| **Commit** | workspace/branch check, batch split, conventional message, push | [references/commit.md](references/commit.md) (§0–§3) |
| **MR/PR** | baseline, pick the intent + template, draft, detect/create/update, read back | [references/mr-pr.md](references/mr-pr.md) (§4–§4.5) |
| **Release** | learn the repo's version/tag convention, tag the shipped commit, create/update the release | [references/release.md](references/release.md) (§6) |
| **Host CLI** | fixed `gh`/`glab` commands + the traps that cost round-trips | [references/host-cli.md](references/host-cli.md) |
| **Voice** | the copy chain (commit → MR → tag/release): how each layer's wording relates, and where the register comes from | [references/voice.md](references/voice.md) |

MR/PR description templates live in [assets/](assets/): [feature-to-integration.md](assets/feature-to-integration.md) verification handoff · [integration-to-production.md](assets/integration-to-production.md) release promotion · [hotfix-to-production.md](assets/hotfix-to-production.md) incident hotfix.

Does **not** replace test-design judgment (see test-design) or TDD rhythm (see superpowers:test-driven-development).

**Core principle: one commit = one reviewable intent with a Conventional-Compliant, non-obscured message; one PR = one shippable story whose description fits its reader and whose claims are verifiable; one release = a tag on the shipped commit plus notes that match the repo's existing convention.**

**Core rules on copy:** commit/PR message format is a hard gate — Conventional Commits, `type(scope): subject`, type from the standard enum, scope from repo convention; **language is flexible** (Chinese / English), following the user's own phrasing/register, not translated into an alien voice ([voice.md](references/voice.md)).

## When to Use

- User says commit / push / "commit and push" / draft or open a PR/MR
- User says tag / cut a version / publish a release, or a promotion MR just merged
- Working tree mixes concerns that should not land in one commit
- Need a PR/MR description with an actionable verification/Test plan

**When NOT to use:** review-only with no ship intent; only designing tests (use test-design). (If a transition gate upstream offered a review and the user declined, proceed on their call.)

## The Iron Law (non-negotiable)

```
1. NEVER commit or push to a protected branch (default: main, master, pro, test — plus any the repo declares).
2. NEVER mix unrelated intents in one commit.
3. EVERY PR/MR description MUST carry an actionable verification section (a Test plan, or the release/hotfix equivalent) for its reader.
4. EVERY commit message MUST be Conventional-Compliant (`type(scope): subject`) and non-obscured; language is free (Chinese/English) but the format is not.
5. NEVER create a NEW MR/PR (or release) without an explicit yes; ALWAYS sync an EXISTING one for this branch/tag (automatic).
6. NEVER trust exit 0 after writing a shared artifact (MR/PR title/body, release notes). Re-read and compare before claiming it landed.
7. NEVER invent a version scheme — follow the repo's tag history; if there is none, ask.
```

**Violating the letter is violating the spirit.** "Just one quick commit on test", "I'll add the Test plan later", and "force push is fine this once" do not count.

## Workflow (when invoked)

Announce "Using commit-and-push to …", then **create one todo per step**:

1. **Confirm workspace + branch + upstream** ([commit.md](references/commit.md) §0) — stop if protected.
2. **Inspect and plan batches** ([commit.md](references/commit.md) §1) — show the plan; execute by default unless ownership is unclear.
3. **Voice** ([voice.md](references/voice.md)) — sample the register from this feature's conversation, not git history; commit reads like the query, MR/release inherit from their upstream.
4. **Commit each batch** ([commit.md](references/commit.md) §2) — stage only that batch; message answers *why*.
5. **Push the feature branch** ([commit.md](references/commit.md) §3) — never force to protected branches; ask before any force.
6. **Draft MR/PR title + description** ([mr-pr.md](references/mr-pr.md) §4) — infer the intent (verification handoff / release promotion / incident hotfix) from the branches' roles, use its [assets/](assets/) template; from *all* commits vs baseline, not only HEAD.
7. **Sync the MR/PR** ([mr-pr.md](references/mr-pr.md) §4.5) — detect an existing MR/PR for this branch (including merged); existing → **update automatically** and read back; none → **ask** before creating.
8. **Tag + release** ([release.md](references/release.md) §6) — only when asked or when a promotion MR merged and this repo releases on merge: learn the repo's convention, tag the **shipped** commit, create/update the release, verify. Skip otherwise.
9. **Report** — paths, commits, push result, MR/PR number + URL, release URL, leftovers.

Do **not** create a new MR/PR or release without an explicit yes; updating an existing one is automatic.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "One big commit is faster" | Reviewers can't bisect or revert cleanly. Batch by intent. |
| "I'll push to test just this once" | Protected means protected. Feature branch + MR. |
| "Test plan later / obvious" | Without a checklist, 'done' is a claim. Always include the verification section. |
| "Force push will clean the history" | Ask first. Never force protected branches. |
| "Hook is annoying — skip with --no-verify" | Fix the cause. Skipping hooks is not shipping. |
| "Amend the failed hook commit" | New commit after fix, unless amend-safety rules all hold. |
| "PR description = last commit message" | PR covers the whole `baseline..HEAD` story. |
| "English-only commits are the only right way" | Format is hard; language is free. Match the user's register (Chinese/English). |
| "Use git history for the user's voice" | History is mostly AI-written. Sample the live conversation instead. |
| "Include the .env so it works on CI" | Secrets never get committed. Warn and skip. |
| "MR/PR already exists — skip the sync" | Existing MR/PR gets synced automatically every push; a stale description is a wrong claim. |
| "Just create the MR/PR, no need to ask" | Creation is irreversible on a shared host — ask first ([mr-pr.md](references/mr-pr.md) §4.5). |
| "`glab api -f description=@file.md` is the same as `-F`" | `-f`/`--raw-field` does not expand `@file` — it writes the literal string `@file.md` and exits 0. Use `-F`, or better `glab mr update -d`. ([host-cli.md](references/host-cli.md)) |
| "exit 0 means the MR/PR body was written" | A shared artifact write is only real after a read-back match. Exit codes lie here. |
| "The branch has commits, so `<integration>..HEAD` is the baseline" | On a promotion MR whose source *is* the integration branch that range is 0. Baseline = the MR's target (production) branch. |
| "Just regenerate the whole MR body from the commit list" | On a release promotion (long-lived release MR) that destroys hand-curated prose/tables. Use incremental re-derivation. |
| "Every MR/PR gets the same description shape" | A verification handoff, a release promotion, and an incident hotfix have different readers — verify steps vs release notes+rollback vs root cause. Use the intent template. |
| "`glab mr view <branch>` finds the MR" | It resolves a branch only when unambiguous; on a many-MR branch it errors. Use `mr list --source-branch`. |
| "Pushing the branch pushed the tag too" | No — `git push origin <tag>` is separate; an unpushed tag has no remote release target ([release.md](references/release.md) §6). |
| "Tag the branch head" | Tag the **shipped** commit on the production branch (usually its merge commit). |
| "Just pick a version number" | Follow the repo's tag history (`git tag --sort=-v:refname`); if there is none, ask ([release.md](references/release.md) §6.1). |
| "`gh release create` again to update the notes" | It errors on an existing tag — use `gh release edit`. (GitLab's `create` updates silently; do it on purpose.) |

## Red Flags — stop immediately

- About to commit/push on `main` / `master` / `pro` / `test` (or repo-protected equivalents)
- Staging unrelated features/fixes/docs in one commit "to be done"
- PR body with no verification section, or only vague "test it"
- Automated block that claims a script ran when it did not
- Using `--force` / `--no-verify` without an explicit user request
- Creating a **new** MR/PR (or release) without an explicit yes
- Skipping the existence check and leaving a stale MR/PR description after a push
- Reporting an MR/PR body (or release notes) as written without a read-back match (exit 0 ≠ written)
- Tagging a feature-branch head instead of the shipped commit; force-pushing a tag
- Inventing a version scheme instead of following the repo's tag history
- `glab api -f/@file`, `--input` without a content-type, `glab mr list --state`, or `glab mr view <branch>` for lookup ([host-cli.md](references/host-cli.md))
- Commit message that only lists file names

**Any hit → stop, return to the Iron Law.**

## Checklist

- [ ] Not on a protected branch; upstream not protected
- [ ] Batches are single-intent; plan shown
- [ ] Each commit message is Conventional-Compliant + non-obscured; language follows user's register; no secrets staged
- [ ] Pushed to `origin <feature-branch>` only
- [ ] Baseline = the MR's target branch (or the repo's integration/default branch when none); `baseline..HEAD` non-empty; counts from `git rev-list --count`
- [ ] Intent inferred from the branches' roles + repo naming (not literal names); matching [assets/](assets/) template used
- [ ] Title + Summary cover **all** commits vs baseline
- [ ] The verification section has ran/checked + open items, both concrete
- [ ] MR/PR checked for this branch (incl. merged): existing → synced automatically (incremental for release promotion); none → asked before creating (or user declined)
- [ ] MR/PR body **read back and matched** after the write (exit 0 was not trusted)
- [ ] (If releasing) version follows the repo's tag history; the **shipped** commit is tagged; tag pushed; release notes match the repo's format; release verified ([release.md](references/release.md) §6)
