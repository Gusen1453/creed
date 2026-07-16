# Engineering Craft

A composable **software engineering methodology** for coding agents — discipline skills that make agents design, test, debug, and ship like careful senior engineers, not coverage-chasing code generators.

Inspired by the structure of [Superpowers](https://github.com/obra/superpowers) (Iron Laws, rationalization tables, red flags, workflows), but focused on **engineering judgment**: *what* to test, *how* to assert, *when* unit vs integration, *how* to mock without lying to yourself.

[![skills.sh](https://skills.sh/b/Gusen1453/engineering-craft)](https://skills.sh/Gusen1453/engineering-craft)

## Quickstart

```bash
npx skills add Gusen1453/engineering-craft
```

Install one skill:

```bash
npx skills add Gusen1453/engineering-craft --skill designing-test-cases
```

## Philosophy

- **Contracts over coverage** — protect user/caller-observable behavior, not line counts
- **ROI over ritual** — unit-test complex logic; integration-test glue; skip theater
- **Falsifiable tests** — break production code and the test must go red, or delete it
- **Evidence over claims** — assert what callers see; mutate to prove the test works
- **Hard to test = hard to use** — listen to the test; fix design instead of piling mocks

## How it relates to Superpowers

| Layer | Superpowers | Engineering Craft |
|-------|-------------|-------------------|
| Rhythm | Red → green → refactor (TDD) | — |
| Case design | — | What to feed, assert, mock |
| Discipline | Rationalization tables, Iron Laws | Same pattern, applied to test quality |
| Scope | Full delivery workflow | Deep methodology for engineering decisions |

Use both: Superpowers for *when/how to run the cycle*; Engineering Craft for *whether the test is worth writing and whether it actually protects anything*.

## Skills library

### Testing (shipping)

| Skill | Use when |
|-------|----------|
| **designing-test-cases** | Writing/reviewing unit or integration tests; choosing cases, assertions, mocks; resisting coverage theater |

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
  designing-test-cases/
    SKILL.md
```

Each skill is a `SKILL.md` with YAML `name` + `description` (trigger conditions only), following the [Agent Skills](https://agentskills.io) format.

## License

MIT
