---
name: grill
description: Use when starting any creative work — a new feature, behavior change, architecture decision, or non-trivial plan — or when the user says grill / grill-me / brainstorm / pressure-test a design, and no code should be written until the design is agreed.
---

# Grill

## Overview

Turn a rough idea into an **approved design** by deciding one thing at a time — then stop. No code until you and the user can say the same thing in plain language.

**Core principle:** Humans own decisions; the repo owns facts. Look up facts. Recommend decisions. Don't implement until the design is confirmed.

**Who you're talking to (one person, two hats):** the user is a **builder who also loves and heavily uses their own product**. So every option must do two things at once:

1. **Translate to product value** — what the experience gains, waits for, or loses — so they don't have to decode jargon to feel the impact
2. **Keep technical precision** — name the real mechanism, tech choice, and trade-off so they keep full control over code and architecture

Never dumb it down into pure "user speak" (they lose grip on the tech), and never hide behind jargon (they lose sight of the product). Say both in one breath: *"picks X so the export stays instant for you, at the cost of an extra queue we have to run."*

**Voice:** A CTO talking to themselves — fluent in the code, honest about what the user will feel.

## When to Use

- Before building a feature, changing behavior, or shaping architecture
- User says "grill me", "brainstorm", "pressure-test this", "help me design…"
- A plan or spec still has soft spots or dependent decisions

**When NOT to use:** pure bugfix with known root cause; mechanical renames; user already approved a written spec and only wants **write-plan** / shipping next.

## The Iron Law (non-negotiable)

```
1. ONE question per message. Never a bulk questionnaire.
2. EVERY option MUST carry a letter marker A/B/C/D… (sequential; escape hatch gets the next letter).
3. EVERY multiple-choice question MUST mark exactly one recommended option in the option label.
4. Frame every option in ONE breath: product-experience impact AND the precise tech mechanism/choice — never jargon alone, never vague "user speak" alone.
5. NO implementation (no code, scaffolds, or implementation skills) until the user confirms shared understanding.
6. Look up facts in the environment; only put DECISIONS to the user.
```

**Violating the letter is violating the spirit.** "Just a quick scaffold while we talk" and "I'll ask five questions at once to save turns" do not count.

## Voice rules (product value + technical precision, together)

Every option makes three things clear in one line:

1. **Product experience** — what using the product feels like: faster, safer, one fewer click, no half-done state
2. **The precise mechanism / tech choice** — the actual approach (queue, index, cache, port/adapter…), named plainly, not buried
3. **Cost we accept** — time, ops, debt, or "what we skip this round"

Never sacrifice one for the other:

| Too obscure (lost product) | Too vague (lost tech control) | Right — both, in one breath |
|----------------------------|-------------------------------|------------------------------|
| "Better separation of concerns" | "Cleaner code" | "Split export from login so changing login can't break export — one small module, ~1 extra file" |
| "Improves scalability" | "Handles more users" | "Add a read replica so lists stay instant at 10× traffic; one more DB to run" |
| "More resilient abstraction" | "More reliable" | "Wrap the write in a transaction so a network blip never leaves a half-saved order" |
| "YAGNI suggests deferring" | "Do less for now" | "Ship the single export flow you use daily; skip the admin bulk UI — no one's asked" |

Say the felt outcome and the mechanism side by side. If you can't name the mechanism, you don't understand it yet — go look it up, don't hand-wave.

## Cursor: AskQuestion (required when available)

If the **AskQuestion** tool exists (Cursor), use it for every fixed-choice question.

Rules:

- **At most one** `AskQuestion` per assistant message
- Prefer short prompts; put the trade-off in the option labels
- **Every option starts with a letter marker** `A)` / `B)` / `C)` / `D)` … in order (including the escape hatch)
- Include at most one escape hatch as the **last** letter: e.g. `D) Something else (I will type it)` — never two "Other" variants
- **Recommended option MUST be labeled in the option text itself**, stating both the felt outcome and the mechanism
- Also state the recommendation in one short prose line ("I recommend **A** because …")
- If AskQuestion is **unavailable**, ask the same single question in prose with A/B/C/D options, same markers

### Option label recipe

```
A) Recommended: <choice via mechanism> — feels like <product outcome>; we accept <cost>
B) <choice via mechanism> — feels like <outcome>; downside <…>
C) <choice> — …
D) Something else (I will type it)
```

Prose may say "I recommend A" — the letter is the stable handle for replies ("go with B").

Never omit letter markers. Never hide the recommendation only in assistant prose while options stay neutral.
Never reduce an option to a bare tech label ("sync vs async") with no felt outcome — and never to a bare outcome with no mechanism.

## Workflow (when invoked)

Announce "Using grill to …", then **create one todo per checklist item** and complete in order:

1. **Explore context** — files, docs, recent commits relevant to the idea
2. **Scope check** — multiple independent products? Split; grill only the first shippable slice
3. **Grill the decision tree** — one question at a time (§Grill loop)
4. **Propose 2–3 approaches** — value-tied-to-mechanism trade-offs + marked recommendation; if approaches imply different boundaries, note one **solid smell** in the option (do **not** switch to full **solid** yet)
5. **Present design in sections** — plain language; get approval per section
6. **Confirm shared understanding** — explicit user yes
7. **Hand off** — **write-spec** (unless waived) → then **solid** only if new modules/ports/IO edges → **write-plan** → **tdd**. Grill does not run the full solid checklist itself.

Tiny change with no product ambiguity: user may waive the written spec; still get a short verbal design + approval, then **write-plan** or **tdd** (skip **solid** if no new boundary).

## Grill loop (decision tree)

Mental model: the design is a **tree of decisions**. Go depth-first / dependency order so early answers reshape later questions.

For each node:

1. If it's a **fact** (what exists in repo, current API shape, config default) → **look it up**; don't ask
2. If it's a **decision** → ask exactly one question
3. Prefer multiple choice via AskQuestion; letter-mark **A/B/C/D…**; mark **Recommended:** stating both product outcome and mechanism
4. Wait for the answer before the next question
5. Challenge soft assumptions — push back; don't rubber-stamp

Keep going until you can summarize the design in a few crisp bullets (product outcomes + the mechanisms behind them) the user agrees with.

## Approaches (before locking design)

Offer **2–3** approaches as **A/B/C** (plus **D** escape if using AskQuestion). For each, give a mini brief that ties value to mechanism:

- **Product experience:** what daily use feels like / what it costs the user
- **Mechanism & tech choice:** the actual approach, named (so you keep control of the tech)
- **Cost / risk we accept**
- **Fit:** how it sits in the current codebase (YAGNI, debt)

Use AskQuestion; letter markers required; one option labeled `Recommended: …`. Pair the felt outcome with the mechanism in each option.

## Design presentation

Once the tree is resolved, present the design in sections. Prefer this order:

1. **Product outcomes** — happy path + main failure in Who/When/Does/Sees language
2. **Mechanisms behind them** — the tech choices that deliver those outcomes, named precisely
3. **Scope** — In / Out this round (Out needs a why)
4. **Key decisions** — what we chose and what we rejected (letter + reason, value + mechanism)
5. **Boundaries** — who owns what data / who talks to whom (plain language)
6. **How we'll know it works** — acceptance in demo language you can turn into tests

After each section, confirm with AskQuestion:

```
A) Recommended: Looks good — continue
B) Needs changes (I'll explain)
C) Something else (I will type it)
```

Scale: a few sentences if simple; up to ~200–300 words if nuanced. Truly small work still needs a short design + approval — "too simple to design" is the anti-pattern that wastes the most time.

## Hard gate → next skill

After approval:

- **Do** invoke **write-spec** (unless user explicitly waives the written doc)
- **Do not** start coding, scaffolding, or calling implementation skills
- **Do not** run full **solid** during grill — only boundary smells in options; Gate solid is after what/why is locked
- Next owner: **write-spec** → (**solid** if new boundaries) → **write-plan**

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I'll ask everything upfront to go faster" | Parallel questions lose dependency order. One at a time. |
| "Options without a recommendation keep me neutral" | Neutrality is laziness. Mark **Recommended:** on one option. |
| "Letter markers are optional chrome" | Letters are the reply handle ("pick B"). Always A/B/C/D…. |
| "Tiny change — skip the design" | Tiny changes hide the worst assumptions. Short design + approval still required. |
| "I'll scaffold while we decide" | Scaffolding is implementation. Hard gate. |
| "User can tell me how the repo works" | Facts → explore. Decisions → ask. |
| "Just say it in user terms — simpler" | The user is also the engineer; hiding the mechanism strips their control. Say both. |
| "Just name the tech — they're technical" | They still shouldn't decode jargon to feel the product impact. Pair value with mechanism. |
| "Skip write-spec — plan is enough" | Plan churns; spec teaches what/why. Default to write-spec. |
| "AskQuestion is optional chrome" | In Cursor, fixed-choice moments use AskQuestion when the tool exists. |

## Red Flags — stop and fix

- Multiple questions in one message
- Options **without** `A)` / `B)` / `C)` / `D)`… letter markers
- Multiple-choice options with **no** `Recommended:` marker
- Options that give a felt outcome but hide the mechanism (user loses tech control)
- Options that give a tech label but no perceivable product consequence
- Writing code or calling build skills before explicit approval
- Asking the user for something visible in the repo
- Neutral "which do you prefer?" with no stance

## Checklist

- [ ] Context explored; facts looked up
- [ ] Scope fits one grill session (or decomposed)
- [ ] One question at a time; AskQuestion used in Cursor when available
- [ ] Every option has an A/B/C/D… letter marker; exactly one `Recommended:`
- [ ] Each option pairs product outcome with the precise mechanism/tech choice
- [ ] 2–3 approaches compared as value-tied-to-mechanism briefs
- [ ] Design sections approved; shared understanding confirmed
- [ ] No implementation yet; hand off to **write-spec** (or waived) → **solid?** → **write-plan**
