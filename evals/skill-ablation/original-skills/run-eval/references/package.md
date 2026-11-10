# Minimal local eval package

Use this stored-output fallback when the project has no established format and needs no executable agent environment. Prefer Harbor for new executable agent tasks, following [format selection](../../create-eval/references/formats.md). It is a fallback for reviewing stored outputs, not an implementation of an agent runtime. Ordinary files and Python's standard library are sufficient; the agent writes narrow scripts in an ignored scratch directory for validation, projection, deterministic checks, and post-verdict comparison.

The package has `rubric.md`, `cases.jsonl`, and `config.json`. Existing `config.yaml` is acceptable when the project already has a parser. Keep run outputs outside these source files. Preserve approved source files unchanged while scoring.

## Config and rubric

The following is an illustrative definition, not a production trust policy:

```json
{
  "schema_version": 1,
  "system": "Reviewed output",
  "eval_version": "1",
  "frozen": false,
  "checks": {
    "code": [
      {"id": "length", "type": "max_chars", "value": 500}
    ],
    "judge": [
      {"id": "source-named", "question": "Does the assertion name its supporting source?", "passing_answer": "yes"}
    ]
  },
  "validation": {
    "min_failure_catch": null,
    "min_acceptable_clear": null,
    "min_cases": null
  }
}
```

Every check has a unique nonempty ID. Semantic questions are independently answerable, have explicit applicability in the rubric, and a passing answer of yes or no. `rubric.md` explains supported boundaries, acceptable alternatives, required evidence, and any approved contrast examples. Contrast examples used for fitting are development material.

Fallback code checks apply to a string `output`:

| Type | Meaning |
| --- | --- |
| `regex_must_match` | PASS iff Python `re.search(pattern, output)` finds a match with default flags. |
| `regex_must_not_match` | PASS iff that search finds none. |
| `max_chars` | PASS iff `len(output) <= value`; value is a nonnegative integer, excluding booleans. |

Reject invalid patterns, duplicate check IDs, unsupported check types, or missing/incorrect parameter types as setup errors. Do not silently skip a configured check. A property beyond these types uses the existing trusted project runner or an explicitly described deterministic predicate; it does not become a substring check for convenience.

## Cases

Each line of `cases.jsonl` is a JSON object. For example:

```json
{"id":"example-001","input":"State one supported assertion.","output":"The value increased.","checks":["length","source-named"],"suite":"development","family":"source-example-001","slice":"source-naming","lane":"adversarial","gold":"FAIL","source":{"kind":"synthetic","note":"Illustrative control; no expert endorsement claimed"}}
```

The illustrated gold is a hand-authored control, not a human calibration label. Production rows must identify their real authority rather than inheriting this example's label.

Required: unique nonempty `id`, recoverable `input`, preserved `output`, nonempty `checks` containing unique configured IDs, `suite`, and `family`. The suite is development, calibration, final-test, regression, or frontier. `slice` and `lane` describe construction when useful; they must be truthful rather than invented to satisfy a quota. A family groups dependent source records or template variants; keep it in one partition for held-out claims.

Optional `context` and `reference` carry permitted task evidence. `gold` is PASS, FAIL, or null; null means unlabeled. Label authority and the exact criterion scope belong in private provenance. A gold label used for judge calibration must cover precisely the checks being aggregated, not only a subset. Per-criterion expert labels need corresponding per-criterion comparison instead of being silently promoted to a whole-case label.

Incomplete inputs, unresolved check applicability, uncertain labels, and missing artifacts stay in a separate incomplete queue. Report the count and reasons. A product run generates a new output; it does not reuse the old output's FAIL label as the new result.

## Blind projection and results

Emit only `{id, input, output, context, reference, checks}` with a fresh opaque run ID, and the selected check definitions. Omit absent optional fields. Keep original IDs, gold, source, family, suite, slice, lane, notes, and all unselected rows private. A contextual clue can still leak a label even after structural projection; inspect the permitted view.

Per-criterion result: run ID, check ID, route, short evidence observation, concise rationale, and PASS/FAIL/UNKNOWN/ERROR. Code results come from code, with any exception recorded as ERROR. Missing required evidence or unresolved applicability is UNKNOWN, not a fabricated answer.

For a case whose required criteria were all evaluated: any decisive FAIL makes the case FAIL; otherwise ERROR or UNKNOWN leaves it incomplete; all PASS makes it PASS. Preserve errors and unknowns even alongside a decisive failure. An unjudged human-only criterion prevents all-PASS completion.

Save a private run manifest with source/config/rubric/payload hashes, actual selected IDs and suites, version/host facts, execution boundary, and paths to results. Freeze a verdict hash before revealing labels. A hash detects later change; it is not a protected store, timestamp authority, or proof the judging context was blind.

Post-freeze comparison scripts verify unchanged hashes and exact case/check coverage before reading gold. Report suite-specific product counts and calibration confusion counts, abstentions, errors, unlabeled rows, and excluded/incomplete rows. Apply a release policy only when explicitly declared and supported by the relevant evidence volume. Final-test opening requires an explicit user instruction, a frozen revision, and a durable exposure record checked before another attempt.
