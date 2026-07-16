# Creed

A **software-engineering judgment** suite for coding agents — not another generic “agent workflow” pack.

Superpowers teaches agents *how to run a delivery loop* (brainstorm → plan → subagents → finish branch).  
**Creed teaches agents how a senior engineer decides** — what is worth building, how to bound it, what is worth testing, what a PR must prove.

> Nothing is true until a test can falsify it. Everything is permitted — except theater.

[![skills.sh](https://skills.sh/b/Gusen1453/creed)](https://skills.sh/Gusen1453/creed)

## Why Creed (vs Superpowers)

Use **both** if you want. Creed’s edge is *closer to real software engineering*, not more agent chrome.

| Creed moat (SE domain) | What agents usually get wrong | Where it lives |
|------------------------|-------------------------------|----------------|
| **1. Test economics** | Unit-test every CRUD/glue path; chase coverage % | `test-design` — complexity in *logic* → unit; in *dependency wiring* → integration; skip theater |
| **2. Contract tests, not mirror tests** | `expected = prodLogic(input)`; assert only mock call counts | `test-design` + `tdd` — hand-written expected; mutation: break code → test must go red |
| **3. SOLID before mocks** | “Hard to test → mock harder” | `solid` — ≥3 mocks is a design smell; ports/adapters, not fake interfaces for tests only |
| **4. Ship gate = executable Test plan** | PR body = last commit message | `commit-and-push` + `review` — mandatory `## Test plan` checklist mapped to *this* diff’s risks |
| **5. Decisions vs facts** | Ask the human how their own repo works; stay “neutral” on choices | `grill` — look up facts; one decision at a time; **every option list marks `Recommended:`** (Cursor AskQuestion) |

**Superpowers remains better at:** multi-harness install, git worktrees, subagent orchestration, long autonomous execution.  
**Creed remains better at:** test ROI, design-for-testability, anti-formalism, PR proof, opinionated engineering choices.

```
Superpowers  ≈  how the agent factory runs
Creed        ≈  how the engineer inside the factory thinks
```

## Quickstart

```bash
npx skills add Gusen1453/creed
```

## Suggested flow

```
using-creed
  → grill → solid → write-plan
  → tdd (+ test-design)
  → debug? → review → commit-and-push
```

## Skills library

### Meta

| Skill | Use when |
|-------|----------|
| **using-creed** | Session start — pick Creed skills; remember the five moats |

### Design & structure

| Skill | Use when |
|-------|----------|
| **grill** | Align on design; one question at a time; AskQuestion + `Recommended:` |
| **solid** | Boundaries, DIP/SRP; fix “too many mocks” with structure |
| **write-plan** | Approved design → bite-sized TDD tasks with exact files |

### Testing

| Skill | Use when |
|-------|----------|
| **tdd** | Red → green → refactor |
| **test-design** | Cases, asserts, mocks; **test economics**; no coverage theater |

### Debug & quality

| Skill | Use when |
|-------|----------|
| **debug** | Root cause + evidence before fixes; verify before “fixed” |
| **review** | Diff vs plan; SOLID + test quality + Test-plan readiness |

### Shipping

| Skill | Use when |
|-------|----------|
| **commit-and-push** | Batched commits; push feature branch; PR with **Test plan** |

### Roadmap

| Area | Planned |
|------|---------|
| Workspace | worktree / finish-branch (optional; Superpowers/worktree commands OK) |
| Deep SE | choosing-test-shape (pyramid vs diamond), recording-based integration |

## Mapping (compatibility)

| Superpowers | Creed analogue | Creed-only depth |
|-------------|----------------|------------------|
| using-superpowers | using-creed | Five SE moats |
| brainstorming | grill | Recommended options + fact/decision split |
| writing-plans | write-plan | Tied to solid + test-design steps |
| test-driven-development | tdd | Requires test-design (economics + mutation) |
| — | **test-design** | Case design / mock ROI |
| — | **solid** | First-class SOLID |
| systematic-debugging + verification | debug | Same spirit, Creed hand-offs |
| requesting-code-review | review | Forces solid + test-design rubric |
| finishing / PR | commit-and-push | Mandatory executable Test plan |

## License

MIT
