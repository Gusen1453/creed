# MR template — Verification handoff ("ready for QA")

**Intent:** a change that needs **independent verification by someone else** before it is accepted. Any branch/target naming can express this (feature or fix → an integration / QA / staging / dev branch — whatever this repo calls it).

**Reader:** the verifier who does **not** have your branch and was not in your head.
**Update semantics:** short-lived. Regenerate from `baseline..HEAD` on every push. No hand-curated prose to preserve.

---

## Title

`type(scope): summary` — Conventional, ≤ ~50 chars, outcome verb first.

## Body

```markdown
## Summary
- What this changes and **why** (the user-visible outcome, not the file list)
- 1–3 bullets covering ALL commits vs the integration baseline

## Impact surface (what touched what)
- **Modules / screens / endpoints affected:** <list>
- **User-facing behavior change:** <before → after>
- **Config / flag / migration:** <name, default, how to toggle> or "none"

## How to verify (do this)
- [ ] <step a verifier runs — URL / command / click path → expected result>
- [ ] <the failure/edge case to also try — empty input, bad value, double-submit…>
- [ ] <the regression you most fear this could cause, and how to check it>

## Test data / environment
- **Where:** <verification env / branch deploy / feature flag on>
- **Data to use:** <account, fixture, seed command>

## Known limits (not in this MR)
- <what this deliberately does NOT do — so the verifier doesn't file it as a bug>

## Test plan

### Automated (ran before commit)
- [x] <command actually run before commit — evidence, not a to-do>

### Acceptance (by the verifier)
- [ ] <observable result the verifier confirms>
- [ ] <the edge case from "How to verify" passes>
```

> Honesty rule: nothing in Automated unless it truly ran. A check you didn't run goes under Acceptance as "to verify".

**Emphasis:** **verification steps + impact surface + known limits.** The verifier's only question is "what do I click to prove this works, and what might it have broken." Rollback is not the point here — not accepting the change is the rollback.
