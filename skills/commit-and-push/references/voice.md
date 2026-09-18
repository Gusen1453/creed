# Voice — the copy chain

Every copy artifact this skill produces — **commit message · MR description · tag message · release notes** — is *one voice at a different distance from the work*. This file is the single source for that voice; the stage references ([commit.md](commit.md), [mr-pr.md](mr-pr.md), [release.md](release.md)) point here instead of restating it.

## The chain

```
query ──► commit ──► MR ──► tag/release
  ╰─────────── anchor ──────────╯
```

Each layer inherits primarily from its **direct upstream**, not from the query. The query is the chain's *anchor* — it fixes the register and proves the human behind the work — but it is **not** every layer's direct source. Writing a release note straight from the query is as wrong as writing it from the commit list.

| Layer | Reader | Answers | Inherits from (direct) | Grammar |
|-------|--------|---------|------------------------|---------|
| **commit** | future you, `git blame` | *why this changed* | **the query** (distance ≈ 0) | imperative |
| **MR** | the reviewer/verifier/releaser | *does it work, what could it break* | **its commits** | declarative, to a peer |
| **tag** | `git log --decorate`, the release UI | *what this version is* | **the MRs it packages** | noun phrase |
| **release** | the product's users, on-call — who may never read a PR | *what this means for me, how to live with it* | **its MRs** | plain narrative |

**Release notes should sound like the MRs, not like the query.** The MR already did one de-jargoning pass for a technical peer; the release is a second pass for a user. By the time work reaches a release it may span weeks and many separate queries — expecting one query's phrasing to survive to the end is a category error.

## Two rules

1. **Facts aggregate up the chain, and must stay traceable.** Every release-note item traces to an MR; every MR claim traces to a commit. Re-derive numbers each layer (`git rev-list --count`), never copy a stale count forward.
2. **Voice normalizes along the chain, and must stay recognizable.** Same speaker, re-voiced per reader — *one voice, four grammars*. Do **not** paste the lower layer's text into the upper (that is the changelog collapse, the same failure as copy-pasting commit titles into release notes).

## Where the register comes from

The register (language + tone) is sampled at the **anchor**, then carried along the chain:

1. **This conversation, this feature's whole lifetime** — every round where the user described the work, corrected the wording, or set direction (not just the last turn). Short, direct, says the outcome; concrete nouns and verbs.
2. **Cross-session memory file** — a settled register from prior work on this repo.
3. **The existing artifact of the same kind** (the last release's notes, the prior MR style) — for cold starts, when there is no live query but a house style exists.
4. **Fallback: the hard rules below** — only when none of the above exist (e.g. the user just said "commit this").

**Why not sample `git log --author`:** in AI-collaborator repos the history is mostly AI-written long clauses (e.g. this repo's `fix(skills): make skill copy English-only Translate…`); sampling it trains the obscurity right back in. Prefer level 1; descend only when a level is absent.

**What "like the user" means — and what it does NOT:**
- It does **not** mean inventing a persona; with no signal, stay neutral and stable (level 4).
- It does **not** override the hard rules — the format gates and the checklist below beat any sampled phrasing.

## Non-obscuring checklist (hard — applies to every copy artifact)

One carve-out: the **outcome-verb** rule below is for commit subjects and the copy that inherits them. An **issue title** is not one of those — a symptom-shaped bug title ("导出空行时崩溃") is the correct form and must not be rewritten into "修复导出崩溃", which describes a fix that has not happened yet. (See the `issue` skill's title rule: outcome-verb for feature/custom, symptom statement for bugs.)

- Subject ≤ ~50 chars of substance; one line
- Start with the **outcome/result verb** (add, ship, route, expose, fix, drop…), not an adjective stack
- No piled modifiers; no vague verbs ("improve", "better", "make nicer"); no file-name dump
- `type` = primary user-visible intent (don't stack every type)
- Match the repo's recent style (language included — Chinese or English as the user writes)
