---
name: using-creed
description: "Use when starting any conversation in a Creed-enabled workspace — establishes how to find and use Creed skills, requiring skill invocation before any creative, test, debug, or ship work."
---

# Using Creed

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a Creed skill might apply, you ABSOLUTELY MUST read and follow it before acting.

No rationalizing past the checklist. Process skills set the approach; then do the work.
</EXTREMELY-IMPORTANT>

## Overview

Creed is a composable software-engineering discipline for agents. Default flow:

```
using-creed
  → grill → solid → write-plan
  → tdd (+ test-design)
  → debug? → review → commit-and-push
```

Nothing is true until a test can falsify it. Everything is permitted — except theater.

## The Iron Law

```
Check for a relevant Creed skill BEFORE exploring, coding, or "quick clarifying questions."
Announce "Using <skill> to …" and follow it. If it has a checklist, one todo per item.
```

**Violating the letter is violating the spirit.**

## Skill map (when to reach)

| Situation | Skill |
|-----------|--------|
| Session bootstrap / which skill? | **using-creed** (this) |
| New feature / architecture / "grill me" / brainstorm | **grill** |
| Boundaries, DIP/SRP, "too many mocks" | **solid** |
| Approved design → task breakdown | **write-plan** |
| Implementing behavior | **tdd** |
| What to assert / mock / theater check | **test-design** |
| Bug / failure / about to say "fixed" | **debug** |
| Before PR / after a task slice | **review** |
| Commit, push, PR + Test plan | **commit-and-push** |

Process order when several apply:

`grill → solid → write-plan → tdd/test-design → (debug) → review → commit-and-push`

## Priority vs other suites

- User instructions (AGENTS.md, rules, explicit asks) win.
- Creed and Superpowers can coexist. Prefer Creed names when both cover the same step (`grill`, `tdd`, `write-plan`, `debug`, `review`) if Creed is installed. Superpowers may still supply worktrees / subagent runners.

## Red Flags — STOP, check skills first

| Thought | Reality |
|---------|---------|
| "Just a simple question / tiny change" | Still a task. Check grill/tdd/solid. |
| "I need context first" | Skills say *how* to gather context. Check first. |
| "I'll explore the repo quickly" | Exploration without the skill skips the gate. |
| "Jump to coding, design is obvious" | **grill** (+ **solid** + **write-plan**) first. |
| "Quick fix without root cause" | **debug**. |
| "Tests after / mock everything" | **tdd** + **test-design**. |
| "Ship without reading the diff" | **review** then **commit-and-push**. |

## Checklist (every turn that does work)

- [ ] Relevant Creed skill identified (or consciously N/A)
- [ ] Skill read/followed; announced
- [ ] Not implementing before grill/plan when building
- [ ] Not skipping tdd/test-design on behavior changes
- [ ] Bugs go through debug; claims have fresh evidence
- [ ] Shipping via review + commit-and-push when asked to commit/push/PR
