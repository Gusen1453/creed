# Creed

A composable **software engineering creed** for coding agents — discipline skills that make agents design, test, debug, and ship like careful senior engineers, not coverage-chasing code generators.

Nothing is true until a test can falsify it. Everything is permitted — except theater.

Inspired by the structure of [Superpowers](https://github.com/obra/superpowers) (Iron Laws, rationalization tables, red flags, workflows), focused on **engineering judgment** across design → test → ship.

[![skills.sh](https://skills.sh/b/Gusen1453/creed)](https://skills.sh/Gusen1453/creed)

## Quickstart

```bash
npx skills add Gusen1453/creed
```

Install specific skills:

```bash
npx skills add Gusen1453/creed --skill grill
npx skills add Gusen1453/creed --skill tdd
npx skills add Gusen1453/creed --skill test-design
npx skills add Gusen1453/creed --skill commit-and-push
```

## Suggested flow

```
grill → tdd (+ test-design) → commit-and-push
```

1. **grill** — align on the design (one decision at a time)
2. **tdd** — red → green → refactor; **test-design** — what to assert/mock
3. **commit-and-push** — batched commits + PR with Test plan

## The Creed

- **Grill before you build** — one decision at a time; mark a recommendation; no code until shared understanding
- **Fail first** — no production code without a failing test you watched go red
- **Contracts over coverage** — protect observable behavior, not line counts
- **ROI over ritual** — unit-test complex logic; integration-test glue; skip theater
- **Hard to test = hard to use** — listen to the test; fix design instead of piling mocks
- **One commit, one intent** — every PR carries an actionable Test plan

## How it relates to Superpowers

| Layer | Superpowers | Creed |
|-------|-------------|-------|
| Design interview | brainstorming | `grill` |
| TDD rhythm | test-driven-development | `tdd` |
| Case / assert / mock quality | (lightly in TDD) | `test-design` |
| Shipping | finishing a branch / PR | `commit-and-push` |

Use both suites if you want; Creed is the judgment layer with short, intuitive skill names.

## Skills library

### Design

| Skill | Use when |
|-------|----------|
| **grill** | Before creative work: decision-tree interview; 2–3 approaches; approved design; Cursor AskQuestion with `Recommended:` on options |

### Testing

| Skill | Use when |
|-------|----------|
| **tdd** | Implementing features/fixes — failing test first, watch RED, minimal GREEN, REFACTOR |
| **test-design** | Choosing cases, assertions, mocks; resisting coverage theater (companion to `tdd`) |

### Shipping

| Skill | Use when |
|-------|----------|
| **commit-and-push** | Batch commits; push feature branch; draft PR/MR with **Test plan** |

### Roadmap (planned)

| Area | Planned skills |
|------|----------------|
| **Testing** | choosing-test-shape, mutation-checking, recording-based integration |
| **Debugging** | evidence-first diagnosis |
| **Review** | reviewing-tests-for-formalism |
| **Meta** | writing-discipline-skills |

## Skill structure

```
skills/
  grill/
  tdd/
  test-design/
  commit-and-push/
```

Each skill is a `SKILL.md` with YAML `name` + `description` (trigger conditions only), following the [Agent Skills](https://agentskills.io) format.

## License

MIT
