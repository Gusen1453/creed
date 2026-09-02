# Example: Batch Import Spec

**Status:** Draft
**Date:** 2026-08-31
**Owner:** Data Engineering

## 1. One-liner

Users can upload a CSV of securities and import them into the holdings table in one shot, instead of adding rows one by one.

## 2. User scenarios

### Happy path
- **Who:** Analyst
- **When:** They have a file of 100 instrument codes
- **Does:** Uploads the CSV, clicks Import
- **Sees:** A success message and 100 rows in holdings

### Failure / edge
- **Who:** Analyst
- **When:** The CSV has 500 rows (the spec's stated max)
- **Does:** Uploads, clicks Import
- **Sees:** All 500 rows imported

## 3. Scope

**In:**
- CSV upload and parse
- Batch insert into holdings
- Duplicate detection on (user_id, instrument_code)

**Out (this round):**
- Incremental sync / scheduled re-runs — infrequent, single-batch use assumed

## 4. Decision log

| Decision | Chose | Rejected | Why |
|----------|-------|----------|-----|
| File size limit | 500 rows max | Unlimited | Analysts complained big uploads timeout |

## 5. Acceptance

- [ ] Upload a valid 100-row CSV → rows appear in holdings
- [ ] Upload a CSV with a duplicate instrument_code → duplicate is rejected, the rest import

## 6. Constraints

- Max 500 rows per file
- CSV is UTF-8, header row required

## 7. How we'll build it (short)

A background worker reads the CSV, validates rows, and inserts them with a single `INSERT ... ON CONFLICT DO NOTHING`. The UI calls the import endpoint and polls a status field until done.