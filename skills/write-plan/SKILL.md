---
name: write-plan
description: "Use when you have an approved design or clear requirements for multi-step work, before touching production code — break the work into bite-sized TDD tasks with exact files, interfaces, and verification steps."
---

# Write Plan

## Overview

Turn an approved design into an **implementation plan** a forgetful agent can execute without inventing scope.

**Core principle: each task is independently testable; steps are 2–5 minutes; TDD is the default micro-cycle.**

**REQUIRED UPSTREAM:** **grill** (and **solid** for non-trivial boundaries) should already have produced shared understanding. Do not plan while product decisions are still open.

**Announce:** "Using write-plan to …"

## When to Use

- After grill/spec approval, before coding
- Multi-file or multi-step features
- User asks for an implementation plan / task breakdown

**When NOT to use:** single-line fix with obvious one-test cycle (go straight to **tdd**); pure exploration.

## The Iron Law

```
NO CODING FROM A VAGUE PLAN.
Every task lists exact files, a failing-test step, a verify-red step, minimal impl, verify-green, and a commit step (or explicit why commit is deferred).
```

## Workflow

1. **Scope check** — multiple independent subsystems? Split into separate plans (one shippable slice each).
2. **File map** — list create/modify/test paths and one-line responsibility each (**solid**: clear boundaries).
3. **Task breakdown** — bite-sized; fold scaffolding into the task that needs it.
4. **Write the plan file** — default `docs/creed/plans/YYYY-MM-DD-<feature>.md` (user path overrides).
5. **Self-review** — no TBD, tasks have Interfaces + verification commands, YAGNI.
6. **User gate** — ask them to skim the plan before execution.
7. **Hand off** — execute with **tdd** + **test-design** (optionally Superpowers subagent-driven-development / executing-plans).

## Plan header (required)

```markdown
# <Feature> Implementation Plan

> **For agents:** Use Creed **tdd** + **test-design** per task. Optional: Superpowers subagent-driven-development / executing-plans.

**Goal:** <one sentence>

**Architecture:** <2–3 sentences>

**Tech Stack:** <key libs>

## Global Constraints

- <verbatim constraints from spec: versions, naming, platforms, …>

---
```

## Task template

````markdown
### Task N: <Name>

**Files:**
- Create: `path/to/file.ts`
- Modify: `path/to/existing.ts`
- Test: `path/to/file.test.ts`

**Interfaces:**
- Consumes: <signatures from earlier tasks>
- Produces: <names/types later tasks rely on>

- [ ] **Step 1: Write the failing test** (apply **test-design**)
- [ ] **Step 2: Run it — expect FAIL for the right reason**
- [ ] **Step 3: Minimal implementation** (**tdd** GREEN; **solid** boundaries)
- [ ] **Step 4: Run tests — expect PASS**
- [ ] **Step 5: Commit** (or defer with reason; ship later via **commit-and-push**)
````

Inline the critical test/impl snippets when they clarify the API; don't dump novels.

## Granularity

| Good task | Bad task |
|-----------|----------|
| One behavior + its test cycle | "Implement auth" |
| Exact paths | "Update the server stuff" |
| Independently reviewable | Must finish Task 5 to know if Task 2 worked |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "We'll figure paths while coding" | That's how scope creeps. Lock files in the plan. |
| "One big task is fine" | Reviewer can't reject half. Split. |
| "Skip test steps — we'll TDD later" | Later = never. Steps include RED/GREEN. |
| "Plan is the design doc" | Design = what/why; plan = who touches which file when. |

## Checklist

- [ ] Design approved (grill); solid considered
- [ ] Plan file written with header + tasks
- [ ] Each task: files, interfaces, RED→GREEN→commit
- [ ] User reviewed plan (or explicitly waived)
- [ ] Ready for tdd execution

## Hand-off

- Execute → **tdd** + **test-design**
- Stuck on structure → **solid**
- Done shipping → **review** then **commit-and-push**
