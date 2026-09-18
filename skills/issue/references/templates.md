# Templates — which one, and where it comes from

How the issue skill picks the skeleton for a draft, and what the optional copy-to-repo step does.

## §1 Which template

Three tiers, all plain Markdown, all live in [../assets/](../assets/):

| Tier | File | Fields |
|------|------|--------|
| bug report | `bug-report.md` | symptom / steps to reproduce / expected vs actual / environment |
| feature request | `feature-request.md` | background / expected outcome / acceptance / rejected alternatives |
| custom | `custom.md` | background / what is wanted / boundaries |

Pick by what the user described, not by wording: something broken → bug; something that should become possible → feature; neither → custom. A bug report gets no "expected outcome" section pushed into it, and a feature request gets no repro steps.

## §2 Where the skeleton comes from — repo-local first

**Read the file and put its content into the draft body. Do NOT pass the CLI's `--template` flag** — it cannot work non-interactively (see [host-cli.md](host-cli.md) §1).

### First, identify the host — ask the CLI to resolve *this repo*

Two separate questions, in this order. Do not collapse them: "which host is this" and "can I talk to it" have different answers and different fallbacks.

**(a) Which host is this?** Ask each CLI to resolve the repo behind `origin`:

```bash
git remote get-url origin        # what repo are we talking about
gh   repo view > /dev/null 2>&1; echo $?   # 0 → GitHub
glab repo view > /dev/null 2>&1; echo $?   # 0 → GitLab
```

`[measured]` The four combinations separate cleanly:

| Probe | in a GitHub repo | in a GitLab repo |
|---|---|---|
| `gh repo view` | **0** | 1 (*"none of the git remotes … point to a known GitHub host"*) |
| `glab repo view` | 1 (*"None of the git remotes … correspond to the GITLAB_HOST"*) | **0** |

- `gh` resolves it → **GitHub**
- `glab` resolves it → **GitLab** (this is how a self-hosted instance is recognised)
- **both** resolve it → ambiguous: the repo has more than one remote, or a mirror config. **Ask the user which host this issue belongs on** — do not pick one. `git remote -v` shows what is configured; naming the two candidates is enough for them to answer. Picking silently means a public issue can land on the wrong host.
- neither → **unrecognised** (step 3 below)

**Use a probe that reads `origin`.** `[measured]` `glab api version` is *not* one — it returns 0 inside a GitHub repo, because it only asks the instance this machine is configured for and never looks at the remote. Using it would label a GitHub repo "GitLab" whenever `gh` happens to be logged out, and would send `-R` commands to the configured instance instead of the one `origin` points at — filing a public issue into the wrong place.

**Do not decide by the hostname's spelling.** A self-hosted GitLab is usually named after the company, not the product — a hostname like `git.example.com` says nothing about which CLI answers for it. A "does the URL contain gitlab" test would call that repo unrecognised and refuse to file, even though the CLI works against it.

**Do not infer the host from which template directory happens to exist**, either. Mirrors, forks and CI-ported repos routinely carry a stray `.github/` inside a GitLab project; going by directory would pick GitHub's command and GitHub's copy-in path for a GitLab repo. The host decides everything downstream: which template directory to read, which CLI to invoke, and where a copy-in would write.

**(b) Can I talk to it?** Only once the host is known. A missing or logged-out CLI makes the probe in (a) fail too, so an *unrecognised* result has two possible causes — tell them apart before concluding:

```bash
gh   auth status    # silent/error → gh has no credentials
glab auth status    # silent/error → glab has no credentials
```

If a CLI has no credentials, the host is **not** unrecognised — it is unknowable from here. Say which CLI needs attention, and hand over the draft **plus the command for whichever host the user names** (`create.md` §6). Do not guess the host to fill the gap.

Note the limit of this check: `auth status` says whether credentials exist, not whether they are for *this* instance. Logged into gitlab.com while `origin` points at a self-hosted instance reads as "no usable credentials for this repo" — which lands on the safe side (hand over the draft) but is worth saying out loud rather than reporting as an unrecognised host.

The same `origin` is what you state in the confirmation (`create.md` §3).

### Then resolve the skeleton

1. **Repo-local template.** Probe only this host's directory, and use the first file in it that matches the request:
   - GitHub → `.github/ISSUE_TEMPLATE/`
   - GitLab → `.gitlab/issue_templates/`

   Use the repo's **section names** as written — they may differ from the built-in ones (e.g. "Actual behaviour" instead of "Expected vs actual"). Strip the front matter; keep the body.
2. **Built-in `assets/`** — the tier table above.
3. **Host unrecognised**: do not probe for templates and do not offer the copy-in step. Compose the body from the tier table's fields — and because [host-cli.md](host-cli.md) only documents `gh` and `glab`, **hand the composed draft to the user instead of filing it** (see `create.md` §6). Composing is still useful: it is the artifact they paste.

Read the whole local template before filling it — if it has sections the user's description does not cover, leave the placeholder rather than deleting the section (the repo owner put it there on purpose).

## §3 Optional: copy the templates into the repo

Only when the user explicitly agrees. What it does:

- Writes the **three** tiers into the **one** directory matching this repo's host:
  - GitHub repo → `.github/ISSUE_TEMPLATE/` ← `bug-report.md`, `feature-request.md`, `custom.md`
  - GitLab repo → `.gitlab/issue_templates/` ← the same three files
- **Never writes the other host's directory** — a GitLab template sitting in a GitHub repo is a dead file, and `commit-and-push` would have to carry it forever.
- Appends one line to each copied file, saying it is synced from the creed skill and that the source is the place to edit:

  `<!-- Synced from the creed `issue` skill. Edit the skill's assets/ copy instead. -->`

  This is the **only** HTML comment allowed in a template; the built-in `assets/` files contain none (see the constraint below).

After copying, **say plainly that these three files are not committed yet** — they are untracked working-tree changes, and the next `commit-and-push` will pick them up. Do not commit them as part of this skill's work.

Skip the whole step, and say why, when:

- the current branch is protected (`main` / `master` / `pro` / `test`, or the repo's equivalents) or HEAD is detached — the files would land on the wrong base;
- the host is unrecognised;
- the user did not ask for it (this step is opt-in, never offered as the default).

## §4 Constraints on template files

- Front matter has `name` / `about` / `labels`. **`labels` stays empty in the built-in files** — label sets differ per repo, so the value is filled from the target repo's actual labels at use/copy time, and never invented.
- No HTML comments in the built-in files. They are read as documents (by people, and by the web form), where comments are visible noise.
- Placeholders use `<angle brackets>` and describe what belongs there; nothing is left as an empty heading.
