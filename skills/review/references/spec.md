# Review — spec

Rubric for reviewing a **spec** (output of `write-spec`, or any approved design doc). The spec is the parent artifact: a plan, solid, or code that locks onto it inherits everything it got wrong.

**Upstream to check:** the grill-approved design decisions the spec was supposed to lock (written grill summary, or the user's stated decisions). If the upstream is missing, the spec still must be internally coherent.

## Claims worth falsifying

A spec is a set of claims. Pull one row per claim into the claim→case table:

- Every **scenario** in §2 (happy + failure/edge) — claim: "a newcomer can role-play this from the text; the outcome is observable."
- The **In/Out** boundary (§3) — claim: "In and Out are mutually exclusive and total; nothing important falls in the seam."
- Every **acceptance item** (§5) — claim: "a human can demo this and the pass/fail is unambiguous."
- The **mechanism claims** (§7) — claim: "the named mechanism actually delivers the named scenario; it does not contradict §2."
- **Constraint claims** (§6) — claim: "the number/limit is testable and the scenario enforces it."
- **Decision-log claims** (§4) — claim: "each row names what was rejected and why in user-visible terms; nothing re-opened silently."
- **Out-of-scope claims** (skipped this round) — claim: "the 'why skipped' is a decision, not an accident."

## claim→case table scenario packs (inject into each claim)

- **happy path** — walk the scenario start-to-finish in plain words; does the spec let you?
- **boundary** — the smallest/largest/most extreme value the scenario implies; empty list, zero rows, quota hit, deadline, just-out-of-range; does the spec say what happens?
- **extreme** — missing upstream data, permission denied, network drop, midnight/rollover, a user who misreads the UI, 100× load; does the spec still resolve?
- **real case** — a past incident, a user complaint, a regression already suffered; run it through the spec verbatim.

## Spec-specific red flags

- An acceptance item that reads like a feature ("support X") with no observable result
- A scenario whose "Sees" is an adjective ("fast", "reliable") with no number or observable state
- In/Out that overlap (same thing in both) or leave a gap (a real request falls in neither)
- A §7 mechanism that cannot deliver a §2 scenario (the seam between scenario and mechanism)
- "We'll decide later" left as a product decision in the text
- The spec leaks implementation (file paths, "Task 3", RED/GREEN) — belongs in plan, not spec
- An In-scope item with no scenario anywhere (cannot be tested → cannot be reviewed)
- Decision log that records only choices, never the rejected alternative or the user-visible why

## Example finding (three-part, plain words)

- **Claim:** acceptance "export completes in seconds".
- **Scenario:** boundary — a 5,000-row export; extreme — network drops mid-export.
- **Verdict:** WATCH — a user who exports a big sheet will watch the spinner with no number attached, and the spec never says whether a dropped network leaves a half-done state. §5 item 3 names "seconds" with no bound; §2 has no failure case for interrupted export.

## Done

- [ ] Each scenario/acceptance/mechanism/In/Out claim ran through happy + boundary + extreme (+ real case if any)
- [ ] No acceptance reads as a feature; no adjective with no observable result
- [ ] Upstream checked (or WATCH noted for missing upstream)
- [ ] Findings plain-word, three-part
