# Review — solid

Rubric for reviewing a **structure/boundary decision** (output of `solid`: unit naming, dependency arrows, port/interface shapes). This is the discipline that makes the code testable without mock piles.

**Upstream to check:** the spec's promised boundaries. Structure must deliver the spec's behaviors without adding coupling; a boundary the spec never asked for is scope add.

## Claims worth falsifying

- Every **unit's single purpose** — claim: "the name contains no 'and'; there is exactly one reason this unit would change."
- Every **dependency arrow** — claim: "domain/policy depends on ports (abstractions), not on DB/HTTP/FS/SDK concretes."
- Every **port/interface** — claim: "small, caller-shaped; each caller uses all its methods; no 15-method interface for a 2-method caller."
- Every **adapter** — claim: "owns a framework/concrete at the edge; nothing domain-shaped leaks through."
- The **theater check** — claim: "every new interface has a product reason, not only a test reason (a real production adapter exists)."
- The **boundary vs spec** — claim: "the structure delivers the spec's scenarios; it adds no modules the spec didn't imply."

## claim→case table scenario packs (inject into each claim)

- **happy path** — wire a real call through the structure (domain → port → adapter → concrete); does each arrow hold?
- **boundary** — the smallest unit (is it real or invented?); the biggest (God type?); a unit with one caller that uses 3 of its 15 methods (ISP failure).
- **extreme** — add a **second IO path** (a second DB, a new HTTP client): does the existing structure absorb it via a new adapter, or does domain code start importing a concrete? Swap the framework behind an adapter — does anything outside the adapter change? A unit test needing ≥3 mocks — that is the signal the boundaries are wrong, not a reason to add more mocks.
- **real case** — a past coupling incident (a DB migration that forced touching domain code; a second data source that required rewriting the core); replay it.

## Structure-specific red flags

- A package/unit that "knows the whole feature"
- Domain importing an ORM, HTTP client, or UI kit
- A subclass override that weakens an invariant (LSP smell); prefer composition
- A new interface used only in tests (no production adapter) — theater
- A unit test mocking half the system to "isolate"
- Structure bigger than the spec implied (a port for a concrete that has exactly one implementation and no second IO path in sight — YAGNI unless the boundary buys testability)
- An "and" in a unit name

## Example finding (three-part, plain words)

- **Claim:** solid decision "RagPush service owns both building chunks and sending them to the vector DB".
- **Scenario:** extreme — the vector DB vendor changes; boundary — unit tests for chunk-building logic need a mocked HTTP client (3 mocks).
- **Verdict:** BLOCK — when the vendor's SDK changes, whoever edits the push half touches the chunk-building half too (one reason to change, two reasons — SRP); and testing the chunk logic forces mocking the network, which is the DIP signal. The spec only promised "send report chunks to the vector DB", so the service is doing more than the boundary it was given.

## Done

- [ ] Every unit has one named purpose; no "and"
- [ ] Every arrow points inward to policy, not out to IO
- [ ] Ports are caller-shaped; adapters own frameworks; no test-only abstraction
- [ ] Structure traced to spec boundaries (no scope add)
- [ ] Second-IO-path + ≥3-mocks simulations run
- [ ] Findings plain-word, three-part