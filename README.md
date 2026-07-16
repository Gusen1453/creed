# Creed

A composable **software engineering creed** for coding agents — discipline skills that make agents design, structure, plan, test, debug, review, and ship like careful senior engineers, not coverage-chasing code generators.

Nothing is true until a test can falsify it. Everything is permitted — except theater.

[![skills.sh](https://skills.sh/b/Gusen1453/creed)](https://skills.sh/Gusen1453/creed)

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
| **using-creed** | Session start — force Creed skill selection before acting |

### Design & structure

| Skill | Use when |
|-------|----------|
| **grill** | Align on design; one question at a time; AskQuestion + `Recommended:` |
| **solid** | Boundaries, DIP/SRP; fix "too many mocks" with structure |
| **write-plan** | Approved design → bite-sized TDD tasks with exact files |

### Testing

| Skill | Use when |
|-------|----------|
| **tdd** | Red → green → refactor |
| **test-design** | Cases, asserts, mocks; no coverage theater |

### Debug & quality

| Skill | Use when |
|-------|----------|
| **debug** | Root cause + evidence before fixes; verify before "fixed" |
| **review** | Diff vs plan; SOLID + test quality before PR/next task |

### Shipping

| Skill | Use when |
|-------|----------|
| **commit-and-push** | Batched commits; push feature branch; PR with **Test plan** |

### Roadmap

| Area | Planned |
|------|---------|
| Workspace | worktree / finish-branch |
| Execution | execute-plan (optional; Superpowers subagents OK for now) |

## How it relates to Superpowers

| Superpowers | Creed |
|-------------|-------|
| using-superpowers | using-creed |
| brainstorming | grill |
| writing-plans | write-plan |
| TDD | tdd + test-design |
| systematic-debugging + verification-before-completion | debug |
| requesting-code-review | review |
| finishing / PR copy | commit-and-push |
| (implicit design) | solid |

## License

MIT
