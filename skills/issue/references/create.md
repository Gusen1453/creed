# Create — from a sentence to a filed issue

The flow: **identify the host → pick a template → compose the draft and title → search for duplicates → resolve labels → confirm → create → report.** Commands are in [host-cli.md](host-cli.md); host identification and template rules are in [templates.md](templates.md).

Section map (the numbering `SKILL.md`'s workflow points at) — note §3a runs **before** §3's question; it is nested there because its result is one of the three things §3 must state:

| Step | Here |
|---|---|
| identify the host, pick the template | [templates.md](templates.md) §2 |
| compose the draft + title | §1 |
| search for duplicates, show the draft | §2 |
| duplicate hit → route (update / new / cancel), then the update flow | §2a, §2b |
| resolve labels | §3a |
| confirm — **once**, for whichever body §2a routed to | §3 |
| create + read back | §4 |
| report | §5 |
| not filing / failures / copy-in | §6 / §7 / §8 |

The tempting shortcuts and why they fail are in `SKILL.md`'s Rationalization Table — not repeated here.

## §1 Compose the draft (nothing is written to the remote yet)

Fill the chosen template's sections from what the user said.

- **Do not invent.** The bug template's environment field, when it cannot be determined, says **"unconfirmed"** — not a guess. The feature template's "rejected alternatives" says **`none`** when there were none — an invented alternative is worse than an empty one.
- **Keep the draft in the conversation.** Do not write a temp file while drafting — it is only written at the moment of a remote read/write (§4), and deleted afterwards.
- **Nothing about the draft is a remote action.** Until the user says yes, the remote must be untouched.
- If the source was a grill session, the draft's "background" and "expected outcome" come from the design decisions, but the **voice stays the user's own** — not the design note's.

**One capability per issue.** If the session settled two unrelated capabilities, the draft covers the **first shippable slice only**. The second becomes another issue — and only after the user agrees to it.

### The title rule

The title is a **readable statement**, not a Conventional-Commits subject — `type(scope):` does not apply to issues. It takes the anti-obscurity rules **as far as they fit**:

- ≤ ~50 characters of substance; one line
- no stacked modifiers; no vague verbs ("improve", "better", "make nicer")
- no file-name dump

**One exemption: a bug title does not start with an outcome verb.** A symptom-shaped title is the correct form for a defect —

| Right | Wrong |
|---|---|
| 导出空行时崩溃 | 修复导出崩溃 |
| Export hangs when the row list is empty | Fix export hang |

The wrong column describes a fix that has not happened yet, which is exactly what an unfixed bug report must not claim. **Feature and custom titles do start with an outcome verb** (add / allow / route / drop…) — there the request *is* about a future outcome.

This is the rule `commit-and-push/references/voice.md` defers to when it carves issue titles out of its outcome-verb requirement.

## §2 Search for duplicates, then show the draft

Run the duplicate search (host-cli.md §3) with keywords drawn from the template's fields.

- **Zero hits is the normal case** — proceed to show the draft.
- **Hits**: list the three most relevant (title + state + link + one-line summary). If there are more than three, say how many were left out.
  - If the user picks one to compare against, use it.
  - If the user does not pick, **choose the top hit yourself and say which one you chose** — do not stall on the question.
- If a hit is **someone else's issue**, say so before offering "update": rewriting another person's description is a different act from editing your own. Treat another author's issue as "open a new one" / "cancel" by default; only edit it if the user asks for that explicitly.

Then present the **complete draft** (title + body). No hit → the confirmation is §3. A hit → §2a first, because "file a new one or update that one" changes *what* is being confirmed.

### §2a When there is a duplicate: pick the action first, then confirm

A hit adds a **routing question** ahead of the confirmation. It is not the confirmation, and it is not a second confirmation — it decides which body §3 will ask about:

- **Update that issue** → §2b, then §3 confirms *the update*. Usually right when the hit is the same request stated worse or earlier.
- **Open a new one** → §3 confirms *the new issue*, as normal. Right when the hit is adjacent but distinct.
- **Cancel** → §6, nothing is confirmed.

So the user sees at most two prompts on this path: one to route (only when there is a hit), one to confirm (always). **Never confirm twice.**

If the hit is **someone else's issue**, say so as part of this routing question — rewriting another person's description is a different act from editing your own. Default the routing to "open a new one" / "cancel", and take "update" only if the user chooses it after hearing that.

### §2b Updating an existing issue instead of filing

**Before writing anything, save the current body.** Issue edits keep no version history on either host, so this is the only restore point:

```bash
gh   issue view <N> --json body --jq .body > "$TMP/before.md"   # GitHub
glab issue view <N> -F json | jq -r '.description' > "$TMP/before.md"  # GitLab
```

Then build the merged body in `$TMP/body.md` (same temp location as §4 — outside the worktree):

- **Merge, do not replace.** Read `before.md` section by section: where the existing text is more specific than the draft, keep the existing wording; where the draft adds detail the existing body lacks, insert it. State which parts you kept, so the user can see nothing was lost.
- What "more specific" means concretely: a real repro beats a vague one; a named version beats "latest"; an actual error string beats a paraphrase.

§3 then confirms **the merged body**, showing the issue number and target repo, with GitLab's irreversibility caveat intact. Only after a yes:

```bash
gh   issue edit   <N> -F "$TMP/body.md"                 # GitHub — body from a file
glab issue update <N> -d "$(cat "$TMP/body.md")"        # GitLab — inline only
```

Details and traps: host-cli.md §6. Then read back and compare exactly as §4 does (same normalisation, same verdict table). Two extra checks:

- **The issue count must not have changed.** Re-run the §3a-style count before and after: `gh issue list -s all --json number --jq 'length'` / `glab issue list -A -O json | jq 'length'`. If it went **up**, an edit turned into a create — say so immediately; on GitHub delete the stray one (`gh issue delete <N> --yes`), on GitLab it can only be closed and annotated, which is a mistake to report, not to bury.
- **If the read-back is still red after normalising**, the body was mangled. Do **not** re-push the same content hoping for a different result — restore from `before.md` (`gh issue edit <N> -F "$TMP/before.md"`), tell the user the merge could not be written safely, and hand over the merged text for them to paste.

Delete `body.md` **and** `before.md` once the read-back has been judged, and on every failure path.

An update needs no label resolution unless you are also changing labels — and the same rule applies then (§3a: only names already in the repo). An update produces **no new URL**: report the existing issue's URL and say what changed, and skip the branch-name suggestion (§5) if one was already given when the issue was filed.

## §3 Confirm — the gate that cannot be skipped

Ask **once** — for a new issue, or (via §2b) for an update. Three things must appear:

1. **Which repo it goes to** — the `owner/repo` (or `group/repo`) of the current worktree's `origin`. Say it explicitly; the user may be working across several repos.
2. **Which labels it will carry** — see §3a. Say "none" when that is the answer.
3. **On GitLab: that the write cannot be undone.** Measured 403 on both `glab issue delete` and the API (host-cli.md §7) — and issue edits keep no version history on either host, so an update is equally final. Say it in these terms: *once written it can only be closed or edited again, not reverted*. On GitHub a filed issue can at least be deleted; an edit still cannot be rolled back except from the copy in `before.md` (§2b).

Say yes → §4 (new) or §2b's edit command (update). Say no → §6.

### §3a Labels — read the repo's list, never hand a name to the CLI

**On GitLab this step is load-bearing.** Measured: `glab issue create -l <name-that-does-not-exist>` **succeeds — and creates the label.** Nothing errors, and the violation is invisible unless you look. On GitHub the same mistake fails loudly and creates nothing, which is why the rule can be skipped there only by accident.

```bash
gh   label list -R <owner>/<repo> --json name -L 200    # -L defaults to 30
glab label list -R <group>/<repo> -P 100                # -P defaults to 30
```

`[measured]` **Both commands paginate at 30 by default.** Without raising it, a repo with more than 30 labels silently hides the rest — and then a perfectly valid `bug` label reads as "no match" and the issue goes out unlabelled, with nothing to indicate anything went wrong. Raise the page size; if the count comes back at the ceiling, say the list may be truncated rather than concluding "no match".

- Match the draft against **those** names. Use a label only if it appears in the list.
- **No match → file without any label.** A repo with zero labels is normal; carry no label and do not create one.
- If the label list **cannot be read** (offline, permissions), treat it as "no match" — file without a label — and say so in the confirmation. Do not fall back to guessing a name.
- The label goes on the create command (`-l <existing-name>`); if the list came back empty, omit `-l` entirely.

## §4 Execute

Only now write the body to a temp file, create the issue with the command for this host (host-cli.md §2), then read the issue back and compare (host-cli.md §5) — normalising line endings and trailing blank lines first, because both hosts normalise.

Write the temp file **outside the worktree** (the system temp directory), so a crash cannot leave an untracked file in the repo — and so a copy-in in progress is not confused with it. **Keep it until the read-back has been judged**, then delete it: it is the left-hand side of the comparison, and the repair path below needs it. Delete it on every failure path too.

**Reading the result:**

| After normalising | What it means | What to do |
|---|---|---|
| Identical | The write landed cleanly | Report success, delete the temp file |
| **Still differs** | Content was mangled (quoting, escaping, an over-eager shell) | **Say so plainly**, show both sides, and offer to repair it with an edit — the temp file is still the correct body, so `host-cli.md` §6 can push it again. **Do not report success** — a red diff that survives normalising is the signal it exists for. Delete the temp file once the repair has been pushed and re-read, or once the user says to leave it. |

A raw `diff` being red is not evidence of failure; a normalised diff being red **is**.

## §5 Report

**When a new issue was filed**, give the user:

- the **issue URL**;
- a **branch-name suggestion**, default shape `<number>-<short-slug>` (e.g. `123-fix-export-empty-row`). Follow the repo's own convention when it has one — this repo's branches carry no issue number at all, which is exactly why the shape is a *suggestion*.
- the **issue number**, and a line saying that the `Closes #<N>` in the PR and the `Issue: #<N>` in a spec are added by `commit-and-push` and `write-spec` respectively — this skill only supplies the number.

**When an existing issue was updated** (§2b), the shape is different — there is no new URL and no new number:

- the **existing issue's URL**;
- **what changed**: which sections were merged in, and which existing wording you deliberately kept;
- the issue count check's result (unchanged — or, if not, the report from §2b).

Skip the branch-name suggestion on an update; if one was given when the issue was first filed, it still stands.

Do not create the branch. Do not touch the PR or any spec.

## §6 When not to file — and what to hand over instead

- **User says no / not yet.** Hand over the paste-ready draft plus the exact `gh` / `glab` command for their platform. No remote write, no temp file left behind.
- **The repo has issues disabled, or the account lacks access.** Check it rather than inferring: `gh repo view --json hasIssuesEnabled` on GitHub, or the project's `issues_enabled` field on GitLab (`glab api projects/:fullpath`). The attempt confirms it too — `gh` says `the '<owner>/<repo>' repository has disabled issues`; `glab` returns 404/403 on the issue endpoint. Either way — say so plainly ("this repo can't take issues") and hand over the draft. Do not retry variations of the command.
- **The host is unrecognised** (neither `gh repo view` nor `glab repo view` resolves `origin`, per templates.md §2). Compose the draft, then **hand it over** with the plain title + body — do not attempt a command; `host-cli.md` documents none for this case.
- **A CLI has no credentials**, so the probe could not identify the host at all. Say which one (`gh` / `glab`), and hand over the draft plus the command for whichever host the user names — do not guess between them.

## §7 Failure paths

Split by what is actually known:

| What happened | What to do |
|---|---|
| The command never left the machine (not logged in, no such repo) | Report the reason; the draft is still in hand. |
| The command **may have reached the remote** (dropped connection, timeout, 5xx) | **Do not retry.** Search again to see whether an issue actually landed, then let the user decide. Retrying is the shortest path to two issues. |
| The duplicate search itself failed (offline, timeout) | Stop guessing. Hand over the draft and the exact command, and say plainly that the remote state is **unconfirmed** — the user should look before filing. |
| An **update** (§2b) failed or wrote mangled content | Restore from `before.md`, say the merge could not be written safely, and hand over the merged text. Do not re-push identical content. |

**Every one of these paths deletes the temp files** (`body.md`, and `before.md` on the update path). A leftover body file is a failed cleanup, not a detail.

## §8 Optional: copying the templates into the repo

Offer it only when the user asks, and check the branch first:

- On a protected branch (`main` / `master` / `pro` / `test`, or the repo's equivalent) or a detached HEAD → **skip the copy and say why**. The files would land on the wrong base, and switching branches to "fix" that would move the user's working tree without being asked. File the issue anyway — the copy is not a prerequisite.
- Otherwise follow [templates.md](templates.md) §3, and **state that the three files are not committed**.

