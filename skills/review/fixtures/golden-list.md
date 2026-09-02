# Golden list — planted bugs the review must catch

Each fixture below contains known defects. Running `review` against a fixture must produce a finding for **every** planted bug here; a missing row means the skill regressed. This is the skill's own regression test (mutation: break the artifact → review must go red).

## How to run

1. Review `fixtures/flawed-spec.md` with `review` (object: spec). Every spec row below must appear in the report.
2. Review `fixtures/flawed-plan.md` with `review` (object: plan). Every plan row below must appear.
3. Review `fixtures/flawed-code/*` with `review` (object: code). Every code row below must appear.

A planted bug is **caught** when the report names the same scene → impact → location, with verdict WATCH or BLOCK. Verdict wording can differ; the scene and impact cannot.

## Planted bugs

### Spec (`flawed-spec.md`)

| # | Scene → impact → location | Must be at least |
|---|---------------------------|------------------|
| S1 | Duplicate in a 500-row file: spec says "duplicate is rejected, the rest import" (§5) but nothing says *which* rows stay when a duplicate appears at row 10 — the analyst loses rows 11–500 with no warning. | WATCH |
| S2 | Spec claims max 500 rows (§6) but the boundary scenario (§2) also uses 500 as "Sees: all 500 imported" — no case for 501 rows: what does the analyst see when they upload 501? Unstated. | WATCH |
| S3 | Acceptance "upload a duplicate → rejected, rest import" is only demoable if the mechanism (§7) can do that, but §7 says `ON CONFLICT DO NOTHING` which *silently skips* rather than *reports* a rejected duplicate — the acceptance's "rejected" (with a report) is not delivered by the mechanism. | WATCH |
| S4 | No failure/edge scenario for a malformed CSV (missing header, non-UTF-8, blank lines) — a newcomer can't role-play what the analyst sees. | WATCH |
| S5 | "Duplicate detection on (user_id, instrument_code)" is In-scope (§3) but no scenario anywhere exercises the *reporting* of a duplicate — In-scope item with no testable scenario. | WATCH |

### Plan (`flawed-plan.md`)

| # | Scene → impact → location | Must be at least |
|---|---------------------------|------------------|
| P1 | Task 2 Step 3 says batch insert with `ON CONFLICT DO NOTHING` but Task 4 ("detect dupes before insert") is a separate task whose test can't pass — once conflicts are ignored, nothing is ever reported as a duplicate, so Task 4's "repeated code triggers a duplicate report" can never go GREEN. | BLOCK |
| P2 | Task 2 Step 1's test ("insert of 100 rows returns success") asserts nothing about duplicates; it would pass even if the insert silently dropped rows — no contract assert for the batch. | WATCH |
| P3 | Task 1 test asserts "500 rows for a 500-row CSV" but the spec constraint "header row required" is never exercised — the parser must skip the header, and no task tests that the header doesn't become a data row. | WATCH |
| P4 | No task enforces the "Max 500 rows per file" constraint (§6) — a 501-row upload has no task that rejects it. | WATCH |
| P5 | Task 3 has no test file listed (files: Create `app/api/import.py`, Modify `app/main.py`, no `Test:`) — the endpoint ships without a test task, and no RED step is defined for it. | WATCH |
| P6 | No task traces to spec acceptance "duplicate is rejected, the rest import" (which rows survive a mid-file duplicate) — the plan's tasks never answer the spec's one real edge case. | WATCH |

### Code (`flawed-code/parser.py`, `flawed-code/loader.py`)

| # | Scene → impact → location | Must be at least |
|---|---------------------------|------------------|
| C1 | **Real case:** an analyst re-uploads after the endpoint times out. `loader.load` does a plain `INSERT` (no `ON CONFLICT`), so a retried import duplicates every row — the exact "500 duplicate rows" incident the spec was meant to prevent. `loader.py:INSERT`. | BLOCK |
| C2 | A CSV with a duplicate at row 10: the single batch `INSERT` raises on row 10 and the *entire* import aborts — rows 11–500 never insert, contradicting the spec's "duplicate rejected, the rest import". No per-row conflict handling. `loader.py:load`. | BLOCK |
| C3 | Parser never skips the header row, so "user_id,instrument_code" becomes a data row — violates the spec constraint "header row required". `parser.py:parse`. | WATCH |
| C4 | A row with fewer than 2 columns raises `IndexError` and aborts the whole batch — no per-row validation. `parser.py:parse` line indexing. | WATCH |
| C5 | No enforcement of the 500-row cap anywhere — a 501-row file imports all rows. | WATCH |

## Contract with the skill

- Every golden row is mandatory output (severity may be WATCH or BLOCK; scene + impact must match).
- A report that produces findings not on this list is fine (extra findings are the skill working).
- A report that misses any row above = the review skill is RED. Fix the skill, not the fixtures.