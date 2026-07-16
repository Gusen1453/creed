---
name: review
description: "Use when finishing a task, before merge/PR, or after a major change — review the diff against the plan/spec for correctness, SOLID, and test quality (no coverage theater), then fix Critical/Important issues before proceeding."
---

# Review

## Overview

Pressure-check the work product against what was agreed — before the next task or before **commit-and-push**.

**Core principle: review the diff and the contract, not your remembered intentions.**

**Announce:** "Using review to …"

## When to Use

- After each plan task (when executing a **write-plan**)
- After a major feature slice
- Before opening/updating a PR/MR
- When stuck (fresh pass over assumptions)

**When NOT to use:** empty diff; user waived review explicitly.

## The Iron Law

```
1. Critical and Important findings BLOCK progress until fixed or explicitly deferred by the human with reason.
2. EVERY review checks: spec/plan compliance, SOLID boundaries, and test-design quality (no theater).
3. NEVER claim "LGTM" without reading the actual diff (and tests).
```

## Workflow

1. **Gather context** (not session vibes):
   - Plan/spec path or stated requirements
   - `git diff` / `BASE...HEAD` (vs integration branch or task start)
2. **Review dimensions** (checklist below) — prefer a fresh subagent/reviewer when available; otherwise self-review with the same rubric
3. **Report** by severity: Critical / Important / Minor — with file references
4. **Act**: fix Critical + Important; note Minor; push back on wrong findings with evidence
5. **Re-verify** affected tests (**debug** verification gate / **tdd**)
6. **Hand off** to **commit-and-push** when shipping

## Rubric

### Spec / plan compliance

- Does the diff implement the agreed Goal — no silent scope adds?
- Missing tasks or acceptance paths?
- Global constraints respected?

### SOLID

- New coupling to IO from domain?
- God types / fat interfaces / test-only ports?
- See **solid**

### Tests (test-design + tdd)

- Behavior tests exist for new behavior?
- Asserts on contracts, not only mocks?
- Hand-written expected? Mutation-worthy?
- Glue covered by integration where ROI demands?

### Risk / ops

- Error paths, migrations, flags, security boundaries
- Obvious footguns in public API

## Report shape

```markdown
## Review
**Scope:** <BASE...HEAD or paths>
**Verdict:** proceed | blocked

### Strengths
- …

### Critical
- …

### Important
- …

### Minor
- …
```

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "It's a small change" | Small changes break prod too. Diff-read anyway. |
| "Tests pass = good" | Tests can be theater. Check test-design. |
| "I'll review in the PR UI later" | Catch now; later compounds. |
| "Reviewer is wrong so ignore" | Push back with evidence — don't ghost Critical. |

## Red Flags

- Shipping without opening the diff
- "LGTM" with no rubric pass
- Proceeding with open Critical/Important
- Reviewing only production files, ignoring tests

## Checklist

- [ ] Diff + plan/spec in hand
- [ ] Rubric covered (spec, solid, tests, risk)
- [ ] Severities assigned; blockers fixed or waived by human
- [ ] Verification re-run if fixes landed
- [ ] Ready for commit-and-push when shipping

## Hand-off

- Failures found → **debug** / **tdd**
- Structure issues → **solid**
- Ship → **commit-and-push**
