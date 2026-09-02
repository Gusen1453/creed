# Review — code

Rubric for reviewing a **code diff / implementation slice**. The code is a child of the plan (and through it, the spec): it must implement exactly what the plan's tasks claimed.

**Upstream to check:** the plan tasks the diff implements (or, without a plan, the spec/approved design). Each behavior in the diff must trace to an agreed task; anything new is scope add.

## Claims worth falsifying

- Every **new behavior** in the diff — claim: "the plan task said what this should do, and the code does exactly that."
- Every **test** attached to the diff — claim: "a real behavior is asserted (hand-written expected), not a mirror of production logic; breaking the behavior breaks the test."
- Every **error path** — claim: "the failure the code can hit is handled (or explicitly allowed to crash), not silently swallowed."
- Every **boundary the diff touches** — claim: "empty input, max size, null, timeouts, concurrent access don't corrupt state."
- **Idempotency/retry** — claim: "a retried call (network drop, user double-click, job re-run) doesn't duplicate side effects."
- **Security edges** — claim: "no injection, no auth bypass, no secret in the diff."
- **Test-design quality** — claim: "tests assert contracts, not mock call counts; no unit test for pure glue; integration where the wiring is the risk."

## 推演表 scenario packs (inject into each claim)

- **happy path** — the golden call; does the code do what the test says?
- **boundary** — empty collection, zero, first/last element, quota, just-out-of-range, null/absent optional, concurrent writers.
- **extreme** — 100× load, network drop mid-write, permission denied, corrupt input, deadline exceeded, a retry storm, a job re-run from scratch.
- **real case** — the actual bug report / failing repro the change claims to fix; run the fix against it — does the user's exact scenario now pass?

## Code-specific red flags

- `expected = productionLogic(input)` in tests (mirror test — asserts nothing)
- Tests that mock the mocking library / count calls instead of asserting behavior
- Diff reviews that skip the test files (the tests are half the claim)
- Error handling only on the happy path; exceptions swallowed with `except: pass`
- Non-idempotent writes behind a retryable endpoint or job
- A behavior in the diff with no matching plan task (silent scope add)
- State mutation shared across threads/requests without a stated strategy

## Example finding (three-part, plain words)

- **Claim:** diff adds "register user" with a uniqueness check on email, test asserts 'the API returns 201'.
- **Scenario:** boundary — two concurrent registrations with the same email; extreme — a retry of a timed-out request.
- **Verdict:** BLOCK — with check-then-insert, two users clicking signup at the same instant both pass the check and one row wins (one user silently gets 201 but is logged into someone's account); the test asserting 201 alone can't see it. The plan task only promised "register", so the race is untested scope the diff introduced.

## Done

- [ ] Each new behavior traced to a plan task (or spec); no scope add
- [ ] 推演表 rows cover error paths, boundaries, retry/idempotency, security
- [ ] Tests assert contracts (hand-written expected), not mirrors; tests read
- [ ] Real case (if any) injected into the table and replayed
- [ ] Upstream checked (or WATCH noted)
- [ ] Findings plain-word, three-part