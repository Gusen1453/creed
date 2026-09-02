# Review — plan

Rubric for reviewing a **plan** (output of `write-plan`). The plan is a child of the spec: it must faithfully narrow what the spec promised, and every task must be independently executable + testable.

**Upstream to check:** the spec (or approved design) the plan implements. Each plan task must trace to a spec scenario/acceptance. If the upstream is missing, note a WATCH and audit against the stated requirements.

## Claims worth falsifying

- Every **task's "Step 2: run — expect FAIL for the right reason"** — claim: "the test genuinely fails before implementation, and for a reason tied to the missing behavior, not a broken harness."
- Every **task's "Step 4: run — expect PASS"** — claim: "a pass here proves the behavior the task claims; the test asserts the contract, not the implementation mirror."
- Every **task's files** — claim: "paths are exact; the task creates only what it needs; nothing upstream depends on a file this task deletes."
- Every **dependency between tasks** — claim: "task N produces the interface task N+1 consumes, at the exact name/type the plan says."
- The **plan header** — claim: "Goal matches the spec; Global Constraints are verbatim-copied, not paraphrased."
- The **granularity** — claim: "each task is independently reviewable; you do not need Task 5's knowledge to know Task 2 worked."
- **No product decisions re-opened** — claim: "every task executes decisions the spec already made; the plan asks no new product questions."

## 推演表 scenario packs (inject into each claim)

- **happy path** — pick one task and walk it: RED → minimal impl → GREEN; does the plan's own wording survive?
- **boundary** — the exact first/last task; the smallest task (is it trivially skipable but still tested?); the seam between two tasks (who owns the integration?).
- **extreme** — panic mid-plan (kill task 3; does the plan recover?); a task that needs a file the plan never created; a network/CI outage during the red-green cycle; forced re-run from scratch after a bad commit.
- **real case** — a past incident where a plan's ordering or missing interface burned you; replay it.

## Plan-specific red flags

- A "Step 1: write test" with no assert target (what expected value? what behavior?)
- A task with no test file, or a test that would pass before implementation (mirror test / production logic call)
- A task whose RED step could pass for the wrong reason (typo in import, empty test)
- Implicit interfaces — task N "fixes X" with no signature for what task N+1 will import
- A task that changes a file another task will also change (merge/rebase trap)
- An acceptance or task that the spec never promised (silent scope add)
- Global Constraints paraphrased or dropped — the plan drifted from the spec
- Product decisions smuggled in ("maybe also support Y")

## Example finding (three-part, plain words)

- **Claim:** plan task 4: "add pagination to list endpoint, Step 1 write test expecting 20 rows, page size 20".
- **Scenario:** boundary — a page with fewer than page-size rows; extreme — a duplicate sort key straddling two pages.
- **Verdict:** BLOCK — a user on page 2 with a tie-break on the sort key will see a row skipped (or repeated); the task's test only asserts "page 1 returns 20", which a mirror implementation could satisfy by slicing the first 20 without a cursor. The spec's "no duplicates on paged lists" acceptance can't pass with this task.

## Done

- [ ] Every task audited: RED fails for the right reason; GREEN asserts the contract (not the mirror)
- [ ] Every task traces to a spec scenario/acceptance; no silent scope add
- [ ] Interfaces between tasks named; sequences recoverable mid-plan
- [ ] Upstream checked (or WATCH noted)
- [ ] Findings plain-word, three-part