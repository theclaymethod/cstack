# Generate cases, inject failures and hand data to DSPy

Use the reference-only recipes in `.agents/skills/adversarial-cases/references/synthetic-methods.md` and `failure-methods.md`. For optimization data read `.agents/skills/hill-climb/references/data-handoff.md`.

Run `python3 -m methods.run --out eval-runs/methods`. Inspect the native measurements rather than relying only on the overall pass status. Explain the reachable sequence defect, which reduction preserved it, which control rejected a shortcut, and what the detection matrix cannot establish. Keep the original spec/cases/rubric/evaluator fixed.

Inspect the fault records. Distinguish a configured trigger, an actual observed event, a performed perturbation and its surviving state. Explain why an unreachable kill trigger does not test recovery, why the reservation-only stop stays pending, and why a once-only storage error differs from persistent failure.

Inspect the project-local DSPy dataset and its source/lineage manifest. Confirm that proposed labels and stale expectations cannot be exported, model inputs contain no expected criteria, and related cases do not cross partitions. Use the optional environment and `--dspy-check` in [the method guide](../methods/README.md) to validate the real SDK without provider calls. Keep operator fault receipts outside task examples.

If you later run DSPy optimization, first establish the actual DSPy target, model/proposer, budget and independent confirmation policy with the owner. Dataset compatibility is not a measured optimization gain. No fixture label is human approval and no exposed split establishes unseen generalization.
