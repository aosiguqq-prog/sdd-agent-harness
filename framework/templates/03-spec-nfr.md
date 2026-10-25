# Non-functional specification · <product>

> IDs SPEC-N-xx. Turns the NFRs into concrete, testable metrics and mechanisms.

| ID | Category | Metric / requirement (measurable) | Implementation / verification | Source |
|----|----------|-----------------------------------|-------------------------------|--------|
| SPEC-N-01 | Performance | P95 < 300 ms @ 100 concurrent users | load-test script | NFR-001 |
| SPEC-N-02 | Security | all input validated server-side | security review + tests | NFR-002 |
| SPEC-N-03 | Usability | errors show a clear message and a way to recover | scenario tests | |
| SPEC-N-04 | Maintainability | coverage ≥ 80%, zero lint errors | CI gate | |
| SPEC-N-05 | Compliance / privacy | <if applicable> | | |
