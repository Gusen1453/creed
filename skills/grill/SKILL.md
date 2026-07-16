---
name: grill
description: Use when starting any creative work (new feature, behavior change, architecture, or non-trivial plan), or when the user says grill / grill-me / brainstorm / pressure-test a design — before writing code. Relentless one-question-at-a-time interview down the decision tree until shared understanding, then a short approved design.
---

# Grill

## Overview

Turn a rough idea into an **approved design** by grilling decisions one at a time — then stop. No code until the user confirms shared understanding.

Fuses:

- **grill-me / grilling** — decision-tree interview; one question; always recommend an answer; look up facts, don't ask them
- **superpowers brainstorming** — explore context, compare 2–3 approaches, present design in sections, hard-gate implementation, optional spec file

**Core principle: decisions belong to the human; facts belong to the codebase. Don't implement until both of you can state the same plan.**

## When to Use

- Before building a feature, changing behavior, or shaping architecture
- User says "grill me", "brainstorm", "pressure-test this", "help me design…"
- A plan still has soft spots or dependent decisions

**When NOT to use:** pure bugfix with known root cause; mechanical renames; user already approved a written spec and only wants implementation/planning next (`writing-plans` / `commit-and-push`).

## The Iron Law (non-negotiable)

```
1. ONE question per message. Never a bulk questionnaire.
2. EVERY multiple-choice question MUST mark exactly one recommended option in the option label.
3. NO implementation (no code, scaffolds, or implementation skills) until the user confirms shared understanding / approves the design.
4. Look up facts in the environment; only put DECISIONS to the user.
```

**Violating the letter is violating the spirit.** "Just a quick scaffold while we talk" and "I'll ask five questions at once to save turns" do not count.

## Cursor: AskQuestion (required when available)

If the **AskQuestion** tool exists (Cursor), use it for every fixed-choice question.

Rules:

- **At most one** `AskQuestion` per assistant message
- Prefer short prompts; put nuance in option labels
- Include at most one escape hatch: `Something else (I will type it)` — never two "Other" variants
- **Recommended option MUST be labeled in the option text itself**, e.g.:
  - `Recommended: Keep it sync — simpler, matches current gateway`
  - `Async worker (not recommended here) — better scale, more moving parts`
- Also state the recommendation in one short prose line above/beside the tool call ("I recommend A because …")
- If AskQuestion is **unavailable**, ask the same single question in prose with A/B/C options, still marking `(recommended)` on one

### Option label recipe

```
Recommended: <choice> — <one-line why>
<other choice> — <one-line tradeoff>
Something else (I will type it)
```

Never hide the recommendation only in assistant prose while options stay neutral.

## Workflow (when invoked)

Announce "Using grill to …", then **create one todo per checklist item** and complete in order:

1. **Explore context** — files, docs, recent commits relevant to the idea
2. **Scope check** — if multiple independent subsystems, decompose first; grill only the first slice
3. **Grill the decision tree** — one question at a time (§Grill loop)
4. **Propose 2–3 approaches** — trade-offs + marked recommendation (AskQuestion)
5. **Present design in sections** — scale length to complexity; get approval per section
6. **Confirm shared understanding** — explicit user yes
7. **Optional: write spec** — `docs/creed/specs/YYYY-MM-DD-<topic>-design.md` (or user-preferred path); self-review; user reviews file
8. **Hand off** — invoke `writing-plans` (or ask user to) — **not** implementation skills

## Grill loop (decision tree)

Mental model: the plan is a **tree of decisions**. Descend depth-first / dependency order so early answers reshape later questions.

For each node:

1. If it's a **fact** (what exists in repo, current API shape, config default) → **look it up**; don't ask
2. If it's a **decision** → ask exactly one question
3. Prefer multiple choice via AskQuestion; always mark **Recommended:** on one option
4. Wait for the answer before the next question
5. Challenge soft assumptions — push back; don't rubber-stamp

Keep going until dependencies are resolved and you can summarize the plan in a few crisp bullets the user agrees with.

## Approaches (before locking design)

Offer **2–3** approaches with trade-offs. Use AskQuestion; one option labeled `Recommended: …`. Lead the prose with why you recommend it (YAGNI, fit to codebase, risk).

## Design presentation

Once the tree is resolved, present the design in sections (architecture, boundaries, data/control flow, failure modes, test approach). After each section, confirm with AskQuestion:

```
Recommended: Looks good — continue
Needs changes (I'll explain)
Something else (I will type it)
```

Scale: a few sentences if simple; up to ~200–300 words if nuanced. Truly small work still needs a short design + approval — "too simple to design" is the anti-pattern that wastes the most time.

## Spec self-review (if writing a doc)

Before asking the user to review the file:

1. No TBD/TODO/vague requirements left hanging
2. No internal contradictions
3. Scope fits one implementation plan
4. Ambiguous requirements pinned to one interpretation

## Hard gate → next skill

After approval:

- **Do** invoke / suggest `writing-plans` (or equivalent plan skill)
- **Do not** start coding, scaffolding, or calling implementation skills

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I'll ask everything upfront to go faster" | Parallel questions lose dependency order. One at a time. |
| "Options without a recommendation keep me neutral" | Neutrality is laziness. Mark **Recommended:** on one option. |
| "Tiny change — skip the design" | Tiny changes hide the worst assumptions. Short design + approval still required. |
| "I'll scaffold while we decide" | Scaffolding is implementation. Hard gate. |
| "User can tell me how the repo works" | Facts → explore. Decisions → ask. |
| "AskQuestion is optional chrome" | In Cursor, fixed-choice moments use AskQuestion when the tool exists. |

## Red Flags — stop and fix

- Multiple questions in one message
- Multiple-choice options with **no** `(recommended)` / `Recommended:` marker
- Writing code or calling build skills before explicit approval
- Asking the user for something visible in the repo
- Neutral "which do you prefer?" with no stance

## Checklist

- [ ] Context explored; facts looked up
- [ ] Scope fits one grill session (or decomposed)
- [ ] One question at a time; AskQuestion used in Cursor when available
- [ ] Every choice list marks exactly one recommendation in the label
- [ ] 2–3 approaches compared with a recommendation
- [ ] Design sections approved; shared understanding confirmed
- [ ] No implementation yet; hand off to planning
