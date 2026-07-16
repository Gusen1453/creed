# Creed

A composable **software engineering creed** for coding agents — discipline skills that make agents design, test, debug, and ship like careful senior engineers, not coverage-chasing code generators.

Nothing is true until a test can falsify it. Everything is permitted — except theater.

Inspired by the structure of [Superpowers](https://github.com/obra/superpowers) (Iron Laws, rationalization tables, red flags, workflows), but focused on **engineering judgment**: *what* to test, *how* to assert, *when* unit vs integration, *how* to mock without lying to yourself — and how to **commit and push** with a real Test plan.

[![skills.sh](https://skills.sh/b/Gusen1453/creed)](https://skills.sh/Gusen1453/creed)

## Quickstart

```bash
npx skills add Gusen1453/creed
```

Install specific skills:

```bash
npx skills add Gusen1453/creed --skill grill
npx skills add Gusen1453/creed --skill test-design
npx skills add Gusen1453/creed --skill commit-and-push
```

## The Creed

- **Contracts over coverage** — protect user/caller-observable behavior, not line counts
- **ROI over ritual** — unit-test complex logic; integration-test glue; skip theater
- **Falsifiable tests** — break production code and the test must go red, or delete it
- **Evidence over claims** — assert what callers see; mutate to prove the test works
- **Hard to test = hard to use** — listen to the test; fix design instead of piling mocks
- **One commit, one intent** — batch commits; every PR carries an actionable Test plan
- **Grill before you build** — one decision at a time; always mark a recommendation; no code until shared understanding

## How it relates to Superpowers

| Layer | Superpowers | Creed |
|-------|-------------|-------|
| Design interview | brainstorming | `grill` (grilling + brainstorming + Cursor AskQuestion) |
| Rhythm | Red → green → refactor (TDD) | — |
| Case design | — | `test-design` |
| Shipping | finishing a branch / PR mechanics | `commit-and-push` with Test plan |
| Discipline | Rationalization tables, Iron Laws | Same pattern, applied to design / test / ship quality |
| Scope | Full delivery workflow | Deep methodology for engineering decisions |

Use both: Superpowers for *when/how to run the cycle*; Creed for *whether the design/test/commit/PR actually protects anything*.

## Skills library

### Design

| Skill | Use when |
|-------|----------|
| **grill** | Before creative work: relentless one-at-a-time interview down the decision tree; 2–3 approaches; approved design; **Cursor AskQuestion with Recommended: marked on options** |

### Testing

| Skill | Use when |
|-------|----------|
| **test-design** | Writing/reviewing unit or integration tests; choosing cases, assertions, mocks; resisting coverage theater |

### Shipping

| Skill | Use when |
|-------|----------|
| **commit-and-push** | Batch commits by intent; write commit messages; push a feature branch; draft PR/MR title + description **with a Test plan** |

### Roadmap (planned)

| Area | Planned skills |
|------|----------------|
| **Testing** | choosing-test-shape (pyramid vs diamond), mutation-checking, recording-based integration |
| **Design** | extracting-testable-cores, boundary-first design |
| **Debugging** | evidence-first diagnosis (complements systematic-debugging) |
| **Review** | reviewing-tests-for-formalism |
| **Meta** | writing-discipline-skills (Iron Law + rationalization table recipe) |

Contributions welcome once a skill has been pressure-tested — prefer quality over a long unread catalog.

## Skill structure

```
skills/
  grill/
    SKILL.md
  test-design/
    SKILL.md
  commit-and-push/
    SKILL.md
```

Each skill is a `SKILL.md` with YAML `name` + `description` (trigger conditions only), following the [Agent Skills](https://agentskills.io) format.

## License

MIT
