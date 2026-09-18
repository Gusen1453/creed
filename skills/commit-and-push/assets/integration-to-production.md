---
name: Ship to production
about: Promoting already-verified work into production
reader: Whoever runs the deploy — they need what ships, what could break, and how to undo it. They may never read the feature MRs.
update: Long-lived; it accumulates features for weeks. Keep the existing prose verbatim, append the new features, refresh only the counts. Never regenerate from the commit list — that turns a curated release note into a changelog.
---

**When this fits:** the branch this repo integrates on going into the branch that serves production — `main`, `master`, `pro`, `prod`, `release`. Judge by the role the branch plays, not its name.

## Title

Name the release, not a commit: `release(vX.Y.Z): <theme>`, or `<integration> → <production>: <date>`.

## Body — fill all four

```markdown
## What ships
- **<Feature A>** — the user-visible change — owner @<handle>
- **<Feature B>** — … — owner @<handle>
- <N> commits, <M> files

## Deploy steps
1. <migrate → deploy → switch the flag on → …>
2. <what to check between steps>

## Rollback
- **Roll back when:** <the signal>
- **How:** <revert commit / flag off / restore point>
- **Costs us:** <data written since deploy? a forward-only migration? nothing?>

## Sign-off
- [ ] Verified on <integration branch> — <link to the QA MR(s) this bundles>
- [ ] Release owner (drives deploy and rollback): @<handle>
```

**Counts:** `git rev-list --count <prod>..<integration>` (keep merges — that is the number the host shows) and `git diff --stat <prod>...<integration>`. Recompute them on every update; a stale count is a wrong claim.

**Do not auto-generate the feature list or the owner handles.** Neither can be derived from git — carry them forward from the existing description, or ask.

## Add a section only when it applies

| Section | Add it when |
|---|---|
| `## Config / env / secrets` — what changed, default, who must set it | production needs a value set before or during deploy |
| `## Migration` — forward step, and what it does on rollback | the release carries a schema or data migration |
| `## Breaking for callers` | an API or contract another team depends on changed shape |
| `## Prod verification` | something can only be checked after deploy, on prod |

No `## Test plan` here — verification already happened on the integration branch. This MR's test is the deploy and the rollback.
