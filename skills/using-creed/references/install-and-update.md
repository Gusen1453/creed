# Install, update, and reinstall the Creed skills

The `skills` CLI installs skills; the repo is only the source. **Editing this repo does not change what an agent loads** — the installed copy is a snapshot taken at install time. This file covers detecting a stale install, and refreshing it safely.

## Where the skills actually live

- **Real install dir (global):** `~/.agents/skills/<name>` (on Windows: `%USERPROFILE%\.agents\skills\<name>`).
- **Agent dirs are symlinks into it.** For Claude Code, `~/.claude/skills/<name>` → `~/.agents/skills/<name>`. Editing the symlink target is editing the install; the agent reads the target.
- **Manifest:** `~/.agents/.skill-lock.json` — keys `version`, `skills`, `dismissed`, `lastSelectedAgents`. Each skill entry records `source` (e.g. `Gusen1453/creed`), `installedAt`, `updatedAt`, and a `skillFolderHash` of the installed content.
- **Skills can also be project-scoped** (inside a repo). Check both before concluding a skill is stale.

## Detect whether the install is behind the repo

Newest-of-three, cheapest first:

1. **CLI knows:** `npx skills update <skill> -g -y` — prints `All global skills are up to date` or upgrades. Safe to run; it only touches this package's skills.
2. **Compare hash to a known release:** the lock's `skillFolderHash` is per skill folder. If the repo has moved since, the hash won't match a fresh install.
3. **Cheapest deep check** — diff a marker file against the repo:
   ```bash
   diff ~/.agents/skills/using-creed/SKILL.md <repo>/skills/using-creed/SKILL.md
   ```
   A stale install shows the repo's newer sections missing (e.g. a `references/` dir that exists in the repo but not in `~/.agents`). **A directory that the repo has but the install lacks is the clearest staleness signal** — the CLI may not add new subfolders on an in-place update.

## Refresh — needs the user's explicit go-ahead

Reinstalling writes to the user's machine and can change any agent's behaviour. **Ask before running it** (offer it, don't just do it), then:

```bash
# 1. remove the package's skills (scoped; other skills untouched)
npx skills remove <skill1> <skill2> ... -g -y

# 2. reinstall from the repo
npx skills add <owner>/<repo> -g -y --skill '*' --agent '*'
```

- Prefer the remove+add pair over `update` when the release **added new files** (e.g. a new `references/` dir) — a plain update may not materialise them.
- `--skill '*' --agent '*'` reinstalls every skill for every agent. To match the user's existing set instead of widening it, read `lastSelectedAgents` from the lockfile first and pass those.
- **Never** claim a refresh succeeded without re-reading a marker file from the installed dir afterwards (see Verify).

## Verify a refresh

```bash
# content matches the repo
diff ~/.agents/skills/<skill>/SKILL.md <repo>/skills/<skill>/SKILL.md
# new files came across
ls ~/.agents/skills/<skill>/references ~/.agents/skills/<skill>/assets 2>/dev/null
```

Then re-read a sentence you know changed in the new release and confirm it is present.

## Gotchas

| Symptom | Meaning |
|---|---|
| `✗ <skill> → <agent>: does not support global skill installation` | That agent has no global scope (e.g. Eve, PromptScript). Harmless; the others installed fine. |
| A skill's symlink points at a stale target | Editing the repo does nothing until reinstall — the symlink target *is* the install. |
| `skills ls` warns `Skipped … YAML parse error` | That **other** skill's frontmatter is malformed. Not your package; ignore unless it is a Creed skill. |
| Repo edited but agent still behaves the old way | The install is a snapshot. Re-install (with the user's confirmation). |

## Why not just rely on memory

A cross-session memory note is a convenience for one machine. Anything a **future agent** must be able to do — detect a stale install, refresh it, verify it — belongs in the skill itself, where it travels with the package.
