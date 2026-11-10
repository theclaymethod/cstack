# Revisit a prompt during a model migration

Use a disposable workspace. Both model names are deterministic stand-ins; this exercise does not validate a real model upgrade. See [the adapter guide](../simplification/README.md).

Give your agent this request:

> Use `$bitter-lesson` to investigate whether migrating the full prompt from `old-fixture` to `new-fixture` lets us remove inherited complexity. Use `$ablation` for removal experiments and the project-local adapter for actual native execution. Preserve task meaning and the evaluator. Compare the old and new stand-ins with the existing prompt and with one shared simplified prompt. Require zero observed pass regressions and zero quality loss relative to the original and to the new stand-in's existing prompt. Use at most 160 native case executions, reserving sixteen for the four final matrix cells. Save versioned configurations, exact prompt text, actual evidence, a reviewable selected artifact and an illustrative rollout/rollback handoff. No model/network calls or production deployment. Name missing evidence and keep all results scoped to synthetic mechanics.

Check the comparison cells and their actual inputs. A new-model improvement must not hide a simplification regression. The same simplified design should appear in both model rows. Missing cells remain missing, readable cases remain exposed, and a successful offline control does not establish production reliability or authorization to deploy.
