# Independent repair review

The three previously reproduced findings are resolved in the reviewed source. No remaining actionable issue was observed in this focused replay. Candidate sources were not edited.

Reviewed `playground/evaluate.py` SHA-256: `c32b0700566c804bf55d97ae027c5dd3f6de15de87920c9bab26471f8a57b421`.

## Observations

- Interrupted retention: interrupted at `compare_runs` after the real improved proposal completed and its evidence was saved. Before resume, baseline was retained and the complete proposal lacked a decision. Two successive `status` calls recovered proposal 1 as best, with budget fixed at 16 case runs. `run_case` was patched to fail if resume attempted execution. Finish selected proposal 1, produced a nonempty diff, and used the expected total of 24 case runs.
- Standalone summary forgery: changed the regression candidate's summary verdicts, counts, and score to 8/8 while retaining its actual execution traces. Comparison now rejects it with `summary differs from execution trace verdicts`.
- Exact state preservation: changing supplied metadata from numeric `1` to Boolean `true`, both at the top level and nested inside a list/object, now yields FAIL. Reordering object keys while preserving values still yields PASS.
- Valid controls: fresh baseline, improved, and regression candidates passed 4/8, 8/8, and 6/8 development cases. Unmodified run evidence validated. The improved comparison was admissible; the regression comparison rejected `dev-closed` and `dev-unrelated` regressions.
- No improvement: an unchanged baseline proposal reported `no improvement`; finish selected baseline 0, reported `no verified improvement; baseline retained`, and wrote an empty diff. The campaign consumed 24 case runs. Repeating finish did not spend more budget.
- Setup validation: a custom case missing `request.account` failed before candidate execution or output-directory creation, with `request requires text, account, and accounts fields`.
- All 15 native tests passed in the isolated copied project.

## Reproduction and evidence

Run from the chat directory:

```sh
python3 work/review-independent/recheck_fixed.py
```

The script copies the current playground into a fresh review directory and runs focused probes against the copy. This replay's retained artifacts are at:

- `/Users/clayton/Documents/Codex/2026-11-10/in-my-cstack-repo-i-want/work/review-independent/fixed-5fgo0ocy/observations.json`
- `/Users/clayton/Documents/Codex/2026-11-10/in-my-cstack-repo-i-want/work/review-independent/fixed-5fgo0ocy/unittest.stderr.txt`
- `/Users/clayton/Documents/Codex/2026-11-10/in-my-cstack-repo-i-want/work/review-independent/fixed-5fgo0ocy/interrupted/`
- `/Users/clayton/Documents/Codex/2026-11-10/in-my-cstack-repo-i-want/work/review-independent/fixed-5fgo0ocy/no-improvement/`

This was a focused repair review, not another broad attack round. Shared host permissions remain the stated trust boundary; these checks do not establish resistance to a process that rewrites every receipt or validate production/generalization claims. The pending C Stack report link was left to the parent agent as requested.
