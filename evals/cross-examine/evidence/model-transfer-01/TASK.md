# Cancel order 1

Update `state.sqlite` so that the complete `orders` table contains exactly:

| id | status |
| --- | --- |
| 1 | cancelled |
| 2 | shipped |

The starting table contains order 1 with status `pending` and order 2 with
status `shipped`. Its schema is
`orders(id INTEGER PRIMARY KEY, status TEXT NOT NULL)`.
Preserve both rows and their IDs, and preserve order 2's status.
Any implementation achieving the required database outcome is valid.

You may read the task and evaluator files. You may write `state.sqlite`,
`result.json`, and `audit.json`. Evaluator code, including `reset.py`,
`solution.py`, and `verify.py`, is read-only to the evaluated agent.
Reports and audit logs are optional and do not determine success.

The operator runs `python3 reset.py` before an attempt and `python3 verify.py`
afterwards. All scripts run in this directory without arguments.
