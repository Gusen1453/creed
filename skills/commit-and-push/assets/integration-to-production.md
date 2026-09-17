# MR template — Release promotion ("ship to production")

**Intent:** promoting an already-integrated, already-verified line of work into **production**. Any naming can express this (an integration/QA/staging branch → a production branch called `main`, `master`, `pro`, `prod`, `release`… — whatever this repo calls it). It is often **long-lived**: it accumulates many feature sections over weeks.

**Reader:** whoever cuts the release — needs to know **what ships, what could break prod, and how to undo it**. They may never read the individual feature MRs.
**Update semantics:** **incremental re-derivation — do NOT regenerate from the commit list.** Preserve the existing prose sections and hand-curated tables; recompute only the stale numbers (commit/file counts), add a section for the new commits, append new acceptance rows. A full rewrite collapses a curated release note into a changelog.

---

## Title

One line naming the release, not a commit subject: e.g. `release(vX.Y.Z): <theme>` or `<integration> → <production>: <window/date>`.

## Body (preserve this structure across updates)

```markdown
## Release summary
- What this release is for, in one breath (theme / window / scope)
- **Counts:** <N> commits, <M> files — from `git rev-list --count <production-ref>..<integration-ref>` (merges included) and `git diff --stat <production-ref>...<integration-ref>`

## What ships (grouped by feature, not by commit)
- **<Feature A>** — user-visible change; affected modules — **owner @<handle>**
- **<Feature B>** — … — **owner @<handle>**
- (append new features here on each update; keep prior sections verbatim unless their facts changed)

## Owners on the hook for this release
- **Release owner (drives deploy + rollback):** @<handle>
- **Per-feature owners:** listed above — the person to ping if their feature misbehaves in prod

## Changes to shared / risky surfaces
- **Config / env / secrets:** <added/changed, default, who must set it>
- **DB / migration:** <forward + how it behaves on rollback>
- **External contract (API / upstream contract):** <breaking? compatible?>
- **Dependencies / version bumps:** <list>

## Deploy sequence (order matters)
1. <step — migrate → deploy → toggle flag → …>
2. <verification between steps>

## Rollback plan
- **Trigger:** <the signal that means roll back>
- **How:** <command / revert commit / feature-flag off / restore point>
- **Data safety:** <does rollback lose anything? forward-only migration caveat?>
- **Blast radius if we can't roll back:** <…>

## Sign-off
- [ ] Verification on the integration branch passed (<link to the verification-handoff MR(s) this release bundles>)
- [ ] Migration rehearsed on staging
- [ ] On-call notified / release window agreed
```

> No `## Test plan` block here by default — independent verification already ran on the integration branch; this MR's "test" is the **deploy + rollback rehearsal** above. If a specific production-only check exists, add one short `## Prod verification` block after deploy.

**Emphasis:** **release notes grouped by feature, risky-surface list, deploy order, rollback, owners.** Numbers must match the host's own counts (`git rev-list --count` includes merges). Owner = the git user who owns the feature (confirm the host handle if it differs). Do **not** auto-generate the attribution/feature table or the owner handles — carry them forward from the existing description or ask.
