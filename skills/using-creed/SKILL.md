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
grill → solid → tdd (+ test-design) → commit-and-push
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
| New feature / behavior / architecture / "brainstorm" / "grill me" | **grill** |
| Shaping modules, dependencies, testability, "this is hard to mock" | **solid** |
| Implementing after design approved | **tdd** |
| What to assert / mock / whether a test is theater | **test-design** |
| Commit, push, PR/MR copy + Test plan | **commit-and-push** |
| Session bootstrap / which Creed skill? | **using-creed** (this) |

Process order when several apply: **grill → solid → tdd/test-design → commit-and-push**.

## Priority vs other suites

- User instructions (AGENTS.md, rules, explicit asks) win.
- Creed and Superpowers can coexist: Creed owns judgment (grill/solid/test-design/ship copy); Superpowers may own extra mechanics (worktrees, subagents). Prefer Creed names when both cover the same step (`grill` over brainstorming, `tdd` over test-driven-development) if Creed is installed.

## Red Flags — STOP, check skills first

| Thought | Reality |
|---------|---------|
| "Just a simple question / tiny change" | Still a task. Check grill/tdd/solid. |
| "I need context first" | Skills say *how* to gather context. Check first. |
| "I'll explore the repo quickly" | Exploration without the skill skips the gate. |
| "Skill is overkill / I remember it" | Read the current SKILL.md. Skills evolve. |
| "Jump to coding, design is obvious" | **grill** (+ **solid**) first unless user forbade it. |
| "Tests after / mock everything" | **tdd** + **test-design**. |
| "One big commit to test" | **commit-and-push**. |

## Checklist (every turn that does work)

- [ ] Relevant Creed skill identified (or consciously N/A)
- [ ] Skill read/followed; announced
- [ ] Not implementing before grill approval (when building)
- [ ] Not skipping tdd/test-design on behavior changes
- [ ] Shipping via commit-and-push when asked to commit/push/PR
