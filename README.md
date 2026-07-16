# Creed

A composable **software engineering creed** for coding agents — discipline skills that make agents design, test, debug, and ship like careful senior engineers, not coverage-chasing code generators.

Nothing is true until a test can falsify it. Everything is permitted — except theater.

Inspired by the structure of [Superpowers](https://github.com/obra/superpowers) (Iron Laws, rationalization tables, red flags, workflows), focused on **engineering judgment** across design → structure → test → ship.

[![skills.sh](https://skills.sh/b/Gusen1453/creed)](https://skills.sh/Gusen1453/creed)

## Quickstart

```bash
npx skills add Gusen1453/creed
```

Install specific skills:

```bash
npx skills add Gusen1453/creed --skill using-creed
npx skills add Gusen1453/creed --skill grill
npx skills add Gusen1453/creed --skill solid
npx skills add Gusen1453/creed --skill tdd
npx skills add Gusen1453/creed --skill test-design
npx skills add Gusen1453/creed --skill commit-and-push
```

## Suggested flow

```
using-creed
  → grill → solid → tdd (+ test-design) → commit-and-push
```

1. **using-creed** — pick and follow the right skill before acting
2. **grill** — align on the design (one decision at a time)
3. **solid** — boundaries and dependency direction (testable without theater)
4. **tdd** — red → green → refactor; **test-design** — what to assert/mock
5. **commit-and-push** — batched commits + PR with Test plan

## The Creed

- **Check skills first** — don't freestyle past the discipline
- **Grill before you build** — one decision at a time; mark a recommendation; no code until shared understanding
- **Boundaries before mocks** — SOLID so tests don't need a fake universe
- **Fail first** — no production code without a failing test you watched go red
- **Contracts over coverage** — protect observable behavior, not line counts
- **One commit, one intent** — every PR carries an actionable Test plan

## How it relates to Superpowers

| Layer | Superpowers | Creed |
|-------|-------------|-------|
| Bootstrap | using-superpowers | `using-creed` |
| Design interview | brainstorming | `grill` |
| Structure | (implicit) | `solid` |
| TDD rhythm | test-driven-development | `tdd` |
| Case / assert / mock | (lightly in TDD) | `test-design` |
| Shipping | finishing a branch / PR | `commit-and-push` |

## Skills library

### Meta

| Skill | Use when |
|-------|----------|
| **using-creed** | Session start / any task — force Creed skill selection before acting |

### Design

| Skill | Use when |
|-------|----------|
| **grill** | Before creative work: decision-tree interview; approved design; Cursor AskQuestion with `Recommended:` on options |
| **solid** | Module boundaries, DIP/SRP, "too many mocks" → fix structure |

### Testing

| Skill | Use when |
|-------|----------|
| **tdd** | Implementing — failing test first, watch RED, minimal GREEN, REFACTOR |
| **test-design** | Cases, assertions, mocks; resisting coverage theater |

### Shipping

| Skill | Use when |
|-------|----------|
| **commit-and-push** | Batch commits; push feature branch; PR/MR with **Test plan** |

### Roadmap (planned)

| Area | Planned skills |
|------|----------------|
| **Planning** | write-plan |
| **Debugging** | debug (evidence-first) |
| **Review** | review |
| **Workspace** | worktree / finish-branch |

## Skill structure

```
skills/
  using-creed/
  grill/
  solid/
  tdd/
  test-design/
  commit-and-push/
```

Each skill is a `SKILL.md` with YAML `name` + `description` (trigger conditions only), following the [Agent Skills](https://agentskills.io) format.

## License

MIT
