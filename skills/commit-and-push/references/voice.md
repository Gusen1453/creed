# Voice — who each piece of copy is for

This skill writes four things: **commit message · MR description · tag message · release notes**. Same work, four readers. This file is the single source for that; the stage references ([commit.md](commit.md), [mr-pr.md](mr-pr.md), [release.md](release.md)) point here instead of restating it.

| Writing | For | Should answer | Written from |
|---|---|---|---|
| **commit** | future you, running `git blame` | why this changed | the user's own request — almost their words |
| **MR** | the person who verifies or ships it | does it work, what could it break | its commits |
| **tag** | anyone reading `git log --decorate` | what this version is | the MRs it packages |
| **release notes** | users and on-call, who never read the MR | what this means for me | its MRs |

## Two rules

1. **Re-derive the facts at each step, don't copy them.** Every release-note line traces back to an MR, every MR claim to a commit. Recount with `git rev-list --count` rather than carrying a number forward — a stale count is a wrong claim.
2. **Re-say it in the new reader's terms, don't paste.** Pasting commit titles into release notes is how a release note becomes a changelog. By the time work ships it may span weeks and many requests, so the release notes should sound like the MRs, not like the original request.

## Where the wording comes from

Use the first of these that exists:

1. **This conversation** — how the user described the work across the whole feature, not just the last message.
2. **Memory** — a settled style from earlier work on this repo.
3. **The last artifact of the same kind** — the previous release's notes, the prior MR's shape.
4. **Nothing to go on** → stay neutral and plain. Do not invent a persona.

**Don't sample `git log --author`.** In AI-collaborator repos the history is mostly AI-written long clauses (this repo has `fix(skills): make skill copy English-only Translate…`) — sampling it trains the padding right back in.

## Say it plainly (applies to every piece of copy)

- One line, ≤ ~50 chars of substance
- Start with the **result verb** — add, ship, route, expose, fix, drop — not a stack of adjectives
- No vague verbs ("improve", "better", "make nicer"), no piled modifiers, no list of file names
- `type` = the main user-visible intent; don't stack every type that applies
- Language follows the user (Chinese or English); the `type(scope):` format does not bend

**One exception — bug issue titles.** A symptom title ("crashes when exporting an empty row") is correct and must not be rewritten into result-verb form ("fix export crash"), which describes a fix that hasn't happened yet. See the `issue` skill's title rule.
