# Tag and release (§6)

The final half of **commit-and-push**: after a release MR has merged (or the user asks to cut a version), tag the shipped commit and publish a release. The commit/push side is [commit.md](commit.md); the MR side is [mr-pr.md](mr-pr.md); raw CLI is [host-cli.md](host-cli.md).

**Trigger:** the user asks to tag / cut a version / publish a release, or a promotion MR just merged and this repo releases on merge.

## §6.1 Learn this repo's release convention first (facts, not rules)

Version schemes and release-note styles are repo-specific. Read them before inventing:

```bash
git tag --sort=-v:refname | head -10          # existing tags → the version scheme (v1.2.3? date-based? v0.x.0?)
for t in <last-3-tags>; do echo "$t: $(git cat-file -t "$t")"; done   # annotated (tag obj) vs lightweight (commit)
gh release list            # or:  glab release list        # prior releases: title + notes style
gh release view <last> --json name,body,tagName,isLatest   # the notes format to match
```

Match what exists: version numbering, annotated-vs-lightweight tag, release **title** pattern, and notes **sections**. If the repo has no prior convention, ask the user rather than picking one.

## §6.2 Decide the version

- Follow the observed scheme, not SemVer dogma. If tags go `v0.5.0 → v0.6.0`, the next is `v0.7.0`.
- Bump the segment the repo's own history suggests (features → minor here; a hotfix-only release might warrant a patch if the repo uses one).
- **Uncertain → ask.** A wrong version is cheap to fix but confusing to consumers.

## §6.3 Tag the right commit

Tag **what actually shipped** — normally the merge commit on the production branch, not your feature branch head:

```bash
git fetch origin
git rev-parse origin/<production>          # the commit to tag (e.g. the merge commit just merged)
git tag -a <version> <sha> -m "<version> — <one-line theme>"    # annotated, matching the repo's style
git push origin <version>                  # the tag must be pushed explicitly; pushing the branch does NOT push tags
```

- Use `-a` when the repo's tags are annotated (check §6.1). Lightweight only if the repo uses those.
- The tag message: one line naming the theme — it is what `--notes-from-tag` would surface.

## §6.4 Publish the release

Write the notes to a temp file first (reproducible + readable), matching the repo's prior release format — for voice, the release inherits from **its MRs**, not directly from the query ([voice.md](voice.md)). Common shape: **What changed** (grouped, plain language) / **Files** / **Prior release** link — but follow *this* repo's actual sections.

```bash
# GitHub
gh release create <version> --title "<title>" --notes-file "$NOTES" --latest
# GitLab
glab release create <version> --name "<title>" --notes-file "$NOTES" --ref <sha>
```

**Detect before creating (same rule as MRs):**

```bash
gh release view <version> --json tagName,url    # errors / 404 if none
glab release view <version> -F json
```

- **Existing release → update it, don't re-create:** `gh release edit <version> --notes-file "$NOTES"`. On GitLab, `glab release create` itself **updates** an existing release (its help: "Create a new GitLab release, **or update an existing one**") — but be deliberate, not silent.
- **No release → create** (as above). This is a shared, visible artifact: it is created on the user's explicit go-ahead, same as an MR.
- `--latest` / latest-flag: only on the newest version; check the prior release's `isLatest` so you don't demote an intended-latest.

## §6.5 Verify (exit 0 is not evidence)

```bash
gh release list | head -3
gh release view <version> --json tagName,isLatest,url
git ls-remote --tags origin <version>        # the tag really reached the remote
```

Confirm tag pushed + release published + notes landed. Report the release URL.

## Traps

| Trap | Reality |
|---|---|
| Pushing the branch also pushes the tag | No — `git push origin <tag>` is a separate command; an unpushed tag has no remote release target. |
| Tagging your feature branch head | Tag the **shipped** commit on the production branch (usually the merge commit). |
| `gh release create` on an existing tag | Errors; use `gh release edit`. (GitLab's `create` silently updates — do it on purpose.) |
| Inventing a version/numbering | Follow the repo's tag history; if absent, ask. |
| Non-ASCII / rich notes in `--notes "<inline>"` | Shell-quoting hazards; write to a file and use `--notes-file`. |
| Personal handle in release notes/credits | Use the git user by default; confirm with the user if the host handle differs ([host-cli.md](host-cli.md)). |
