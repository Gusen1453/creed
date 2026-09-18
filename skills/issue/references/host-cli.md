# Host CLI — issue operations (gh / glab)

Fixed commands for issue create / search / update / delete, plus the traps that were **measured on this machine**. Everything below is marked with how it was established:

- **`[measured]`** — the command was actually run and its output compared.
- **`[source-checked]`** — read from the CLI's source or `--help`; not run.

Hosts where the measurements were taken: **gh 2.97 with GitHub `Gusen1453/creed`** and **glab 1.114 with a self-hosted GitLab, `code.comein.cn`, project `llm/opencode`**. Carry these versions and the markers into any file that quotes these facts — **never restate a `[source-checked]` fact as `[measured]`**.

Shared gh/glab mechanics live in [commit-and-push's cheatsheet](../../commit-and-push/references/host-cli.md): credential setup (`gh auth setup-git`), `glab api`'s `-f` vs `-F`, and the read-back-after-write rule. Do not duplicate them here.

## §1 Templates cannot be passed on the command line

**Do not use `--template`.** Compose the body yourself (see [templates.md](templates.md)).

`[measured]` `gh issue create --template` under a non-interactive shell fails every way:

| Attempt | Result |
|---|---|
| `-t <title> -T "Bug report"` | `must provide --title and --body when not running interactively` |
| …plus `-F body.md` | `` `--template` is not supported when using `--body` or `--body-file` `` |
| …plus `-e` | `--editor or enabled prefer_editor_prompt configuration are not supported in non-tty mode` |

`[source-checked]` Root cause in `pkg/cmd/issue/create/create.go`:

```go
opts.Interactive = !opts.EditorMode && !(titleProvided && bodyProvided)
```

A template can supply neither title nor body, so `titleProvided && bodyProvided` is false and the command always lands in the interactive branch — which a non-tty shell rejects.

`[measured]` On GitLab, `--template` and `-d/--description` are a **mutually exclusive flag group**:

```
If any flags in the group [template description] are set none of the others can be;
[description template] were all set.
```

`--template <name> --no-editor` alone does create an issue (template body only) — but then the body is whatever the template says, so the user's content has nowhere to go. Not a usable path.

## §2 Create

**`-R <owner>/<repo>` is optional when the worktree's `origin` is already the target.** It appears below because the probes ran from an unrelated worktree; drop it when running from the repo itself, keep it when filing across repos.

```bash
# GitHub — body from a file (never inline -b: shell quoting mangles multi-line CJK/backticks)
gh issue create -R <owner>/<repo> -t "<title>" -F body.md [-l <label>]

# GitLab — inline only; there is no --description-file
glab issue create -R <group>/<repo> -t "<title>" -d "$(cat body.md)" [-l <label>] -y
```

- `[measured]` Both print the new issue's URL to stdout. **Neither has `--json`.** To get the number, parse the URL's trailing segment.
- `[measured]` `gh issue list -s all -L 1 --json number` also works, but only when the new issue is the newest — parse the URL when it matters.
- Write the body to a temp file **only at the moment of creating** (nothing is pre-written during drafting), and delete it afterwards **including on every failure path**.
- `-y` on GitLab suppresses the confirmation prompt. **Do not add it reflexively** — the "ask before creating" rule is the skill's, not the CLI's; the CLI prompt is not the gate.

## §3 Duplicate search

```bash
gh   issue list -R <owner>/<repo> -s all -S "<keywords>"
glab issue list -R <group>/<repo> -A --search "<keywords>" --in title,description
```

- **Neither `-s all` nor `-A` may be omitted.** `[measured]` Both CLIs default to **open only** in a non-interactive shell — a closed duplicate would be invisible and the skill would offer to create a second one.
- `[measured]` On GitLab the `-A` difference is stark: the same query returns 0 rows without it and the closed match with it.
- `[measured]` Both searches cover the **description**, not just the title.
- `[source-checked]` The result set is issues only — `gh`'s issue search pins the entity (`is:pr` qualifiers hard-error with "cannot use pull request search qualifiers with `gh issue list`"), and `glab issue list` never returns merge requests.
- `[source-checked]` `glab issue list` has **no `--state` flag** (`Unknown flag: --state`). Use `-A` / `--opened` / `--closed`.
- Keywords come from the template's fields, not from the whole draft — a broad sweep matches unrelated issues forever.

## §4 Labels — the two hosts behave oppositely

**GitHub validates; GitLab silently creates.**

- `[measured]` `gh issue create -l no-such-label` → hard failure, **no issue created**: `could not add label: 'no-such-label' not found`.
- `[measured]` `glab issue create -l probe-autocreate-label` → **the issue is created AND the label is created** (`glab label list` went 0 → 1).

Consequence: to honour "map only to existing labels, never create one", **on GitLab you must fetch the label list first** and map against it — handing the name straight to the CLI violates the rule.

```bash
glab label list -R <group>/<repo> -P 100              # -P defaults to 30 — raise it
gh   label list -R <owner>/<repo> --json name -L 200  # -L defaults to 30 — raise it
```

`[measured]` Both paginate at **30** by default. Leaving the default on a repo with more labels hides valid ones, and a legitimate label then reads as "no match" with nothing to show anything went wrong.

A repo with **zero** labels is normal (`llm/opencode` is one): the draft carries no label at all, and nothing is created.

## §5 Read back after writing — and expect normalisation

```bash
gh   issue view <N> -R <owner>/<repo> --json body --jq .body
glab issue view <N> -R <group>/<repo> -F json | jq -r '.description'
```

`[measured]` **Neither round-trips byte-for-byte**:

| Host | What comes back |
|---|---|
| GitHub | the source **plus one trailing newline** (86 B → 87 B) |
| GitLab | the source with **every LF converted to CRLF** (45 B → 47 B) |

So the comparison is "identical **except for the known normalisation**": normalise line endings and trailing blank lines on both sides first, *then* `diff`. A raw `diff` will always be red, and reporting that as a write failure is wrong.

The same applies to the local copy of a repo template: GitLab's read-back will show CRLF where the file has LF.

## §6 Editing and closing

```bash
# GitHub
gh issue edit <N> -R <owner>/<repo> -F body.md

# GitLab — inline, same caveat as create
glab issue update <N> -R <group>/<repo> -d "$(cat body.md)"
```

(As in §2, `-R` is only needed when the target is not the current worktree's `origin`.)

`[measured]` Both write the body correctly (GitLab: backticks, `→`, CJK all survive). **Neither keeps any version history** — an edit overwrites and there is no "previous body" to recover, on either host. So the caller must save the old body itself before editing (`create.md` §2b does exactly that). Also measured: the **`N-` / `#N` link key does not exist anywhere in either repo's branch names** — `Gusen1453/work` on GitHub, `feat/mcp-loading` and `develop/tool-harness-hooks` on GitLab. The issue number therefore has to be carried forward from the session, not recovered from the branch.

## §7 Cleaning up a mistake — only GitHub lets you

`[measured]` `gh issue delete <N> --yes` works; the issue disappears and the repo returns to its previous count.

`[measured]` **GitLab refuses.** Both `glab issue delete <N>` and `glab api -X DELETE projects/.../issues/<N>` return **403 Forbidden** for a non-owner account. The only recovery is:

```bash
glab issue close <N> -R <group>/<repo>
glab issue update <N> -R <group>/<repo> -d "<this issue was created by mistake — please delete it>"
```

**This asymmetry is the strongest reason the create step asks first, and it must be said out loud in the GitLab confirmation.** On GitHub a mistake is one command away from gone; on GitLab it stays visible forever.
