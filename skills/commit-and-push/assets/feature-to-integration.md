---
name: Ready for QA
about: A change that someone else has to verify before it is accepted
reader: The verifier — they do not have your branch and were not in your head
update: Short-lived. Regenerate the whole body from `baseline..HEAD` on every push; nothing here is hand-curated.
---

**When this fits:** a feature or fix heading into whatever branch this repo verifies on — `test`, `dev`, `staging`, `qa`, `develop`. Judge by the role the branch plays, not its name.

## Title

`type(scope): summary` — Conventional, ≤ ~50 chars, outcome verb first.

## Body — fill all four

```markdown
## What changed
- <the user-visible outcome and why — covering every commit in this MR, not just the last one>

## Where to check
- **Environment:** <test env / branch deploy / the flag to switch on>
- **Account / data:** <login, fixture, seed command>

## What to verify
- [ ] <click path or command → what you should see>
- [ ] <the edge case: empty input, bad value, double submit…>
- [ ] <the nearby thing this could have broken>

## Already ran
- [x] <command that actually ran, and its result>
```

**Honesty rule:** `Already ran` is evidence, not a plan. A check you did not run belongs in `What to verify`.

## Add a section only when it applies

| Section | Add it when |
|---|---|
| `## Behaviour change` — before → after | existing behaviour moved, so the verifier's memory is now wrong |
| `## Config / migration` — name, default, who sets it | there is a new env var, flag, or DB migration |
| `## Out of scope` | something looks unfinished on purpose — say so, or it gets filed as a bug |

Leave a section out entirely rather than writing "none" — an empty heading is noise the verifier has to read.
