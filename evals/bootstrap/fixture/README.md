# Support routing prototype

The assistant is not implemented yet. There are no production traces. We have requirements discussions and want evals before building the feature. Work locally; no accounts, APIs, or paid model runs are needed.

Existing eval format: JSONL rows in `evals/`, with unique `id`, `input`, `family`, and `expected`. `expected` has `allowed_actions` (a nonempty list of strings) and `ticket_delta` (an integer). The intended action vocabulary is `guidance`, `create_ticket`, or `clarify`.

Existing stored-observation runner:

```sh
python3 runner.py --cases evals/cases.jsonl --observations observations.jsonl
```

An observation row has `case_id`, `action`, and `ticket_delta`. The runner checks the action against the allowed set and compares the ticket count delta. It reports missing observations as ERROR, and grades all expected cases. Stored observations are not executions of the assistant. Preserve the existing suite and runner.
