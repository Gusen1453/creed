# Example: Batch Import Implementation Plan

> **For agents:** Use Creed **tdd** + **test-design** per task.

**Goal:** Allow an analyst to import up to 500 instrument codes from a CSV in one request.

**Architecture:** Background worker validates and inserts; UI polls a status field.

**Tech Stack:** Python, SQLAlchemy, PostgreSQL.

## Global Constraints

- Max 500 rows per file
- CSV is UTF-8, header row required

---

### Task 1: Parse CSV

**Files:**
- Create: `app/import/parser.py`
- Test: `app/import/parser_test.py`

- [ ] **Step 1: Write failing test** — expect `parse()` returns 500 rows for a 500-row CSV
- [ ] **Step 2: Run it — expect FAIL**
- [ ] **Step 3: Minimal implementation** (`csv.reader`, header skip)
- [ ] **Step 4: Run tests — expect PASS**
- [ ] **Step 5: Commit**

### Task 2: Insert rows

**Files:**
- Create: `app/import/loader.py`
- Test: `app/import/loader_test.py`

- [ ] **Step 1: Write failing test** — expect insert of 100 rows returns success
- [ ] **Step 2: Run it — expect FAIL**
- [ ] **Step 3: Minimal implementation** — batch insert with `ON CONFLICT DO NOTHING`
- [ ] **Step 4: Run tests — expect PASS**
- [ ] **Step 5: Commit**

### Task 3: Expose import endpoint

**Files:**
- Create: `app/api/import.py`
- Modify: `app/main.py`

- [ ] **Step 1: Write failing test** — POST `/import` with a CSV returns 201
- [ ] **Step 2: Run it — expect FAIL**
- [ ] **Step 3: Minimal implementation** — wire parser + loader to the endpoint
- [ ] **Step 4: Run tests — expect PASS**
- [ ] **Step 5: Commit**

### Task 4: Duplicate handling

**Files:**
- Create: `app/import/dupes.py`
- Test: `app/import/dupes_test.py`

- [ ] **Step 1: Write failing test** — a CSV with a repeated instrument_code triggers a duplicate report
- [ ] **Step 2: Run it — expect FAIL**
- [ ] **Step 3: Minimal implementation** — detect dupes before insert
- [ ] **Step 4: Run tests — expect PASS**
- [ ] **Step 5: Commit**