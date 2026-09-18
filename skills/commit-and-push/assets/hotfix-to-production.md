---
name: Hotfix
about: A fix that has to reach production now, skipping the verification stage
reader: The on-call engineer approving an out-of-band production change — what broke, why this fixes it, how to back out
update: One-shot and short, usually one commit. Regenerate from `baseline..HEAD` and keep it terse. Do not pad — the reader is mid-incident.
---

**When this fits:** a fix going straight into the branch that serves production, bypassing the verification branch.

## Title

`fix(scope): <the symptom, not the code>` — e.g. `fix(order): duplicate settlement on payment callback`.

## Body — fill all four

```markdown
## What broke
- **Symptom:** <what production actually did>
- **Who was hit, and when:** <scope + time window>

## Root cause
- <the one thing that was wrong — evidence, not a guess>

## The fix, and why it is safe now
- <what this change does, one line>
- **Proof:** <the repro that failed before and passes now — command + result>
- **Also touches:** <blast radius, or "nothing else">

## Rollback
- **How:** <revert this commit / flag off>
- **Costs us:** <does reverting lose or duplicate anything?>
```

If the root cause is not yet proven, say so — write `unconfirmed` and describe what you ruled out. A guessed root cause is worse than an admitted gap (see `debug`).

## Add a section only when it applies

| Section | Add it when |
|---|---|
| `## Why not wait` | the urgency is not obvious from the symptom alone |
| `## Post-deploy checks` | someone must confirm on prod after merge — list the checks |
| `## Follow-up` | a proper fix or regression test is owed on the next release — one line, plus an issue number |

Owner: the git user who made the fix, on the hook until prod is confirmed. Confirm the host handle if it differs from `user.name`, and set them as assignee/reviewer — a body mention does not reliably page anyone ([host-cli.md](../references/host-cli.md)).
