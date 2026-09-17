# MR template — Incident hotfix ("out-of-band production fix")

**Intent:** a fix that must reach **production now**, skipping the normal verification stage. Any naming can express this (a hotfix branch, or a fix cut straight from the production branch → the production branch — `main`, `master`, `pro`, `prod`, `release`…).

**Reader:** the on-call engineer approving an out-of-band production change — needs to know **what broke, why this fixes it, and how to back out fast**.
**Update semantics:** one-shot and short. Usually a single commit; regenerate from `baseline..HEAD` but keep it terse. Do not pad.

---

## Title

`fix(scope): <the symptom, not the code>` — e.g. `fix(order): duplicate settlement on payment callback`.

## Body

```markdown
## Incident
- **Symptom:** <what users/prod actually saw>
- **Impact & window:** <who was hit, from when to when, how bad>
- **Detected by:** <alert / customer report / dashboard>

## Root cause
- <the one thing that was wrong — evidence, not a guess>

## Fix
- <what this change does, in one line>
- **Why hotfix (not wait for the verification stage):** <urgency reason>

## Risk of this fix
- **Blast radius:** <what else this touches>
- **Why it is safe to ship straight to prod:** <test/repro evidence — the exact repro now passes>
- **What it does NOT address:** <follow-up left for the normal release>

## Rollback
- **How:** <revert this commit / flag off — one line, no ceremony>
- **Data safety:** <does reverting lose/duplicate anything?>

## Owner / approval
- **Fix owner (on the hook until prod is confirmed):** @<handle> — the git user; confirm if the host handle differs
- **Approver:** @<handle> (or "self-serve, on-call notified")
- Set as assignee/reviewer so the ping actually lands ([host-cli.md](../references/host-cli.md)).

## Hotfix test plan

### Automated (ran before commit)
- [x] <the failing repro, now passing — command + result>

### Post-deploy verification (do immediately after merge)
- [ ] <the prod check that confirms the symptom is gone>
- [ ] <a guard check that the fix didn't break the adjacent path>
```

**Emphasis:** **root cause, rollback, the repro that proves it.** No feature narrative, no release notes. Follow-up (the "proper" fix / regression test on the integration branch) gets a one-line pointer, not a section.
