# Requirements: <area>

What <area> must do. Each requirement has an ID, a reason, a source, the behaviour in Given, When, Then form, and at least one test scenario. The Then and And lines are the acceptance criteria: each one observable, met or not met.

### R-<AREA>-001 <one behaviour, in a few words>

Why: <the reason in one line, so a reader can judge the requirement without opening its source>.

Source: <the question, goal, constraint, principle or design choice this comes from, by ID>.

- Given <the situation>
- When <what happens>
- Then <what the user or the system sees>
- And <what must not happen, or must not change>

Test scenarios:
- T-<AREA>-001a (anywhere, automated by <test name, or "to write">): <data>, <steps>, <expected result>.
- T-<AREA>-001b (lab, automated by <tool, or "manual" with the reason>): <data>, <steps>, <expected result>.

### R-<AREA>-002 <a failure case: missing, late or wrong data>

Why: <...>.

Source: <...>.

- Given <...>
- When <...>
- Then <...>

Test scenarios:
- T-<AREA>-002a (anywhere, ...): <...>.
