# Host CLI cheatsheet — gh / glab (fixed workflows + traps)

Fixed commands for the MR/PR sync, plus the traps that cost real round-trips. Everything here is verified against `gh` 2.97 and `glab` 1.114 unless marked otherwise. Prefer the CLI subcommands; reach for `glab api` only for something the CLI doesn't cover.

## People — @mentions, assignee, reviewer

`@handle` in the **body** notifies only if that user has access to the repo; the reliable signal is an **assignee/reviewer**, which also puts the MR in their queue.

```bash
# GitHub
gh pr create ... --assignee <login> --reviewer <login>      # repeatable; @me = yourself
gh pr edit <N> --add-assignee <login> --add-reviewer <login>
gh pr comment <N> --body "@<login> your feature broke prod; rolling back"   # urgent ping

# GitLab
glab mr create ... -a <username> --reviewer <username>      # comma-separated or repeated
glab mr update <N> -a <username> --reviewer <username>
glab mr note <N> -m "@<username> your feature broke prod; rolling back"
```

- Handles are **host** usernames. **Default to the git identity** (`git config user.name` / the commit author) — it usually is the right handle.
- The exception is when they differ (e.g. a shared/service commit identity, or a host nickname distinct from `user.name`). That is a **point to confirm with the user**, never to guess — do not derive the mapping from `git log`, and do not invent a handle.
- `@`-mention inside the body text is convenient for a reader but is **not** a substitute for `--assignee`/`--reviewer` when you need someone actually on the hook.

## Release / tag

```bash
# Learn the repo's convention (scheme, tag type, notes style)
git tag --sort=-v:refname | head -10
gh release list ; gh release view <tag> --json name,body,isLatest

# Tag the shipped commit (annotated, matching repo style), then push the tag
git tag -a <version> <sha> -m "<version> — <theme>"
git push origin <version>

# Publish (notes from a file)
gh release create <version> --title "<title>" --notes-file "$NOTES" --latest
glab release create <version> --name "<title>" --notes-file "$NOTES" --ref <sha>

# Update an existing release — never re-create
gh release edit <version> --notes-file "$NOTES"      # GitLab: glab release create <ver> UPDATES an existing release
```

- Pushing a branch does **not** push its tag — `git push origin <tag>` is separate.
- `glab release create` on an existing tag **updates** it (per its help); `gh release create` **errors** — use `gh release edit`.
- Full workflow + traps: [release.md](release.md).

## Detect host + repo roles

```bash
git remote get-url origin            # the repo under discussion
git symbolic-ref refs/remotes/origin/HEAD   # the default branch, without guessing main/master
```

**Which host is it?** Ask each CLI to resolve *this repo* — `gh repo view` exits 0 → GitHub; `glab repo view` exits 0 → GitLab; neither → unknown host. Do not read the hostname's spelling (a self-hosted GitLab is usually named after the company, not the product), and do not use `glab api version` — it ignores `origin` and answers 0 even inside a GitHub repo. (Same rule as the `issue` skill's [templates.md](../../issue/references/templates.md) §2.)

Roles, not names: identify which branch is **integration** (`test`/`dev`/`staging`/`qa`/`develop`…), which is **production** (`main`/`master`/`pro`/`prod`/`release`/`production`…). The MR's own `target_branch` is the ground truth for *this* MR.

## Find the MR/PR for a branch (any state)

```bash
BR="$(git branch --show-current)"

# GitHub — newest PR from this head branch, any state
gh pr list --head "$BR" --state all --json number,title,url,state,baseRefName --jq 'sort_by(.number)|last'

# GitLab — -A is REQUIRED; --state is NOT a valid flag
glab mr list -A --source-branch "$BR" -F json --jq 'sort_by(.iid)|last'
#   narrow to one target:  --jq '[.[]|select(.target_branch=="<prod>")]|sort_by(.iid)|last'
```

- `glab mr list` defaults to **open only** — a merged MR is invisible without `-A`, and you will then wrongly offer to create a duplicate.
- One source branch can map to **many** MRs over time (e.g. a long-lived `test` branch). Pick by `target_branch` then newest `iid`.
- `glab mr list --state open` → **hard error** (`Unknown flag: --state`). Exit code can still be non-zero-looking; don't rely on it.
- Do **not** use `glab mr view <branch>` for branch lookup — it resolves only when unambiguous, else `You must select a merge request: merge request ID number required`.

## Create

```bash
# GitHub
gh pr create --base <target> --head "$BR" --title "<title>" --body-file "$BODY"

# GitLab
glab mr create --source-branch "$BR" --target-branch <target> --title "<title>" -d "$(cat "$BODY")"
```

## Update (preferred path — body via -d from a file)

```bash
# GitHub
gh pr edit <N> --title "<title>" --body-file "$BODY"

# GitLab — byte-exact roundtrip (verified); backticks, →, −, unicode all safe
glab mr update <N> --title "<title>" -d "$(cat "$BODY")"
```

- **Never** `-d -` — opens an interactive editor; a non-interactive agent hangs.

## Read back / verify a write

```bash
diff <(glab mr view <N> -F json | jq -r '.description') "$BODY"   # GitLab
diff <(gh pr view <N> --json body --jq .body) "$BODY"            # GitHub
```

A trailing-newline difference is host normalization — fine. Anything else is a real mismatch.

## Traps (each cost a real incident)

| Trap | What happens | Correct form |
|---|---|---|
| `glab api -f "description=@file.md"` | `--raw-field`/`-f` does **not** expand `@file` → writes the literal string `@file.md`, **exit 0** (silent data loss) | `-F`/`--field` expands `@file`; or just use `glab mr update -d` |
| `glab api --input body.json` without a content-type | HTTP **415** (`The provided content-type '' is not supported`), and the error JSON mixes into stdout so a `JSON.parse` blows up again | add `-H "Content-Type: application/json"` |
| Trusting `exit 0` after writing a body or release notes | The `-f @file` trap exits 0 having written the wrong bytes. Exit codes do not prove content landed | re-read and `diff` against your file (§Read back) |
| `glab mr list --state open` | `Unknown flag: --state` | omit it (default = open) or use `-A` for all |
| `glab mr view <branch>` on a many-MR branch | `merge request ID number required` | `mr list --source-branch` + `-A` |
| `git rev-list --count --no-merges` | undercounts; won't match the host's "N commits" | `git rev-list --count` (merges included) |
| `git push` in a non-interactive shell | `Cannot prompt because user interactivity has been disabled` / `unable to get password` | `gh auth setup-git` (wires gh's credential helper into git for HTTPS), then retry |
| `git push` and expecting the tag to go with it | Tags are not pushed with the branch, so the release has no remote target | `git push origin <tag>` separately |
| `gh release create` on a tag that already exists | Errors out | `gh release edit`. (GitLab's `create` updates silently — do it on purpose) |
| `@file`/`-d` value with a leading space | e.g. `-F 'topics= ["a"]'` — the space is part of the value, sent as a string | keep `=` immediately before `@`/the value |

## gh / glab api field semantics (the underlying rule)

From `glab api --help`:

- `--field` / `-F`: parses JSON (`true`, numbers, `[...]`, `{...}`), and **`@`-prefix reads from a file**; `:`-placeholders (`:fullpath`, `:branch`) are substituted.
- `--raw-field` / `-f`: sends the value as a plain string; **no `@` expansion**, no JSON parsing.
- `--input <file>`: raw request body; needs an explicit `Content-Type` header for JSON endpoints.

Because the failure mode of `-f` is silent (exit 0, wrong content), the standing rule is: **for anything that writes a shared artifact, use the CLI subcommand (`gh pr edit` / `glab mr update -d`), and read it back.**
