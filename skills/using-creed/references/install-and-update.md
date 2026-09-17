# Install, update, and reinstall the Creed skills

The `skills` CLI installs skills; this repo is only the **source**. The install is a
snapshot, so editing the repo changes nothing an agent loads until a reinstall. This
file covers detecting a stale install (by comparing to the **cloud repo**), and
refreshing it safely across agents.

A normal user does **not** have this repo checked out — so every check here works
against the published repo, not a local clone. A maintainer with a checkout can use
the same commands plus a local diff (§verify).

## Where the skills live

- **Install hub (global):** `~/.agents/skills/<name>` — the real files live here once.
- **Manifest:** `~/.agents/.skill-lock.json` — keys `version`, `skills`, `dismissed`, `lastSelectedAgents`. Each entry records `source` (e.g. `Gusen1453/creed`), `skillPath`, `skillFolderHash`, `installedAt`, `updatedAt`.
- **Agent directories are links into the hub, not copies.** `skills` knows each agent's directory and symlinks the skill in (use `--copy` to copy instead). The directories it manages include:
  `.claude/skills`, `.codex/skills`, `.cursor/skills`, `.continue/skills`, `.cline/skills`, `.gemini/skills` (and `.gemini/antigravity`, `.gemini/antigravity-cli`), `.opencode/skills`, `.windsurf/skills`, `.deepagents/agent/skills`, plus kimi variants.
  On a given machine only the agents that were installed to will be populated; the same skill appears as a symlink pointing back to `~/.agents/skills/<name>`.
- **Project scope exists too** (a repo can carry its own skills). Check both before concluding a skill is stale.

## Detect whether the install is behind (compare to the cloud)

No repo needed. `update` itself is the check — it compares each installed skill against the published repo and only changes what differs:

```bash
npx skills update <skill> -g -y     # e.g. npx skills update using-creed -g -y
```

- Output `All skills are up to date.` → the install matches the repo.
- Otherwise it upgrades the stale ones. It works by fetching the repo and recomputing a sha256 over the skill folder's files (`skillFolderHash`), then comparing to the value stored in the lockfile — so it is a real content check, not a timestamp.
- To see what the repo currently offers **without installing**: `npx skills add Gusen1453/creed -l`.

**Maintainer extras (only if you have a local checkout):** `diff ~/.agents/skills/<skill>/SKILL.md <repo>/skills/<skill>/SKILL.md`, or check that a directory the repo added (e.g. a new `references/`) also exists under `~/.agents/skills/<skill>/`. A hub dir missing something the repo has is the clearest staleness signal, because an in-place update may not materialise brand-new files.

## Install the whole set

```bash
npx skills add -y -g Gusen1453/creed
```

- `-g` installs globally (user-level, into `~/.agents/skills`); `-y` skips prompts and auto-detects which agents are present.
- To target specific agents: `--agent claude-code cursor` (or `--agent '*'` for all).
- The skills install as a set; install all of them, not a subset.

## Reinstall / uninstall — needs the user's explicit go-ahead

Reinstalling writes to the user's machine and can change any agent's behaviour.
**Ask before running it** (offer it, don't just do it).

```bash
# 1. remove the package's skills — clears the hub entries AND every agent link
npx skills remove <skill1> <skill2> ... -g -y

# 2. install the set again
npx skills add -y -g Gusen1453/creed
```

- Prefer remove + install over `update` when a release **added new files** (a new `references/` dir, a new skill) — a plain update may not materialise them, whereas a fresh install will.
- `remove` without `-a` cleans **all** agent links; pass `-a <agent>` to scope it to one agent.
- Reinstalling is not agent-specific work: the CLI re-links every agent directory it manages in one pass, so you do not need to uninstall per agent.

## Verify a refresh

```bash
npx skills update <skill> -g -y        # expect: All skills are up to date.
ls ~/.agents/skills/<skill>/            # new dirs (references/, assets/) are present
```

Then re-read a sentence you know changed in the new release and confirm it is present in the hub file.

## Gotchas

| Symptom | Meaning |
|---|---|
| `✗ <skill> → <agent>: does not support global skill installation` | That agent has no global scope (e.g. Eve, PromptScript). Harmless; the others installed fine. |
| Agent still behaves the old way after a repo edit | The repo is only the source; the install is a snapshot. Reinstall (with the user's confirmation). |
| A skill dir in `~/.claude/skills` etc. is a symlink | Normal — it points into `~/.agents/skills`. Editing the target *is* editing the install; the agent reads it. |
| `skills ls` warns `Skipped … YAML parse error` | That **other** skill's frontmatter is malformed. Not this package; ignore unless it is a Creed skill. |

## Supplementary

If the user runs Orca, its skill-sharing can also surface these skills; that is a
convenience view, not the install — the hub above is authoritative.
