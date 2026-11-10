# Project-local generation, failures and DSPy

Validated 2026-11-10 for C Stack 0.7.0. New method guidance is reference-only. Executable demonstrations, optional SDK dependencies and generated data belong to the playground project. The native evaluator, source cases, spec and rubric remain unchanged.

## Implemented and observed

| Method | Actual evidence |
| --- | --- |
| Structured contrasts and reachable sequences | Ten native-format generated cases, including a two-step creation/repeat witness. A declared faulty candidate passes all 12 original cases, then creates a duplicate when it sees its own prior valid output. The conforming candidate passes both steps. Invalid predecessors stop continuation. |
| Structured reduction | Remove unrelated records individually, retain the same duplicate mechanism and rerun legitimate controls. Removing the required creation predecessor loses the mechanism and is rejected. No global or 1-minimality claim. |
| Mutation-guided selection | Three explicit faulty candidates, each evaluated once on the 12 original and ten final generated cases. Three selected witnesses detect the declared catalog. The 66 comparison executions and 29 construction/control executions total 95. All cases are exposed development evidence. |
| Named lifecycle perturbations | Source-pinned named mappings for reservation publication, summary publication and completion publication. Three matching owned-process SIGKILL events/exits. Pending reservations remain charged; complete evidence is retained or recovered without rerunning cases. Clean, observed-noop and armed-unreached controls remain distinct. |
| Storage faults | Once-only and persistent fsync/rename OSError injections using the actual atomic writer, plus no-op controls. Failed writes preserve publication, one-shot retry succeeds, persistent failure retains the original, temporary files are cleaned. These model scoped API errors, not disk exhaustion or power loss. |
| Subprocess failures | Actual deadline, flushed JSON prefix then deadline, valid JSON then nonzero exit and malformed output. Native ERROR classification retains selected denominators. Healthy output passes. |
| Project-local DSPy handoff | Ten examples split into four training and six adaptive validation rows with connected ancestry and exact duplicates kept together. Export/load checks reject proposed labels, stale criteria, input/source changes and changed dataset membership/content. Only request/state enter model inputs. |

The complete method run uses **140 native case executions**, comprising 95 generation/selection and 45 fault/control executions, plus **three owned-process interruptions and two candidate deadlines**. Storage operations are separately recorded and are not candidate executions. The optional SDK check uses **20 deterministic in-process DSPy program invocations** with no model/provider calls. Replays and test invocations consume their own work; these figures describe one complete method run.

## Actual DSPy compatibility

The optional local environment pins DSPy **3.5.0** and its resolved development dependencies. Real Example, Prediction, Module and Evaluate objects run the deterministic support function. Scalar scoring delegates to the native grader; the GEPA-compatible metric returns failed checks and observed/required state deltas. The conforming program receives 100 percent on these ten examples. False creation is FAIL; malformed output and an explicitly supplied execution-error record remain ERROR. Actual subprocess errors are independently executed by the fault experiments.

This validates SDK/data/metric compatibility. No LM, instruction proposer or live optimizer compile ran. Model, mutable DSPy target, cost budget and confirmation policy remain choices for a later campaign. The percentage is a deterministic fixture observation, not an LLM result or an optimization gain.

## Independent use and review

A fresh agent applied the references to a separate account-membership contrast/reduction family, without using the supplied generator as its whole test. Six new cases executed against the original and conforming candidates, plus a valid-output/exit-7 treatment: **13 native subprocess cases**. A separate real DSPy program executed six times; additional metric-only controls checked alternate IDs, wrong account and malformed schema. No interruption/provider/network calls were used. Its [report](evidence/forward-use/REPORT.md) retains source identity, authority, commands and actual outputs; its resume policy is declared metadata, not an implemented guard.

Independent [code review](evidence/code-review.md) found a duplicate-run-label bug that could overwrite the outer case source before native execution refused the old output directory. The fix rejects used labels/paths before reservation or writes. The reviewer independently reproduced the harmless rejection; a regression verifies unchanged source/ledger bytes, spend and call count. Original failing evidence remains in [the reproduction](evidence/duplicate-label/executions.json). This is a local provenance repair, not protection against arbitrary host writes.

## Run it

Create a disposable workspace from the checkout:

```sh
python3 fixtures/playground/scripts/new_workspace.py --out eval-runs/methods-playground
cd eval-runs/methods-playground
python3 -m methods.run --out eval-runs/methods
```

For actual SDK validation, use the optional environment in [the method guide](../../fixtures/playground/methods/README.md). Its requirements stay in the project; the factory excludes `.venv` when copying a workspace. Without `--dspy-check`, the SDK check is explicitly not run. With the environment active:

```sh
python3 scripts/run_cstack_evals.py --suite all --dspy-check --out eval-runs/all-controls
```

All **nine control groups** passed, including **30 native tests**, the original calibration/replays/audits and the methods group with SDK validation. All eight skills pass frontmatter validation. The factory's environment-exclusion behavior was also tested after its update. [Control summary](evidence/validation/summary.json), [native test log](evidence/validation/playground.stderr.txt), [method results](evidence/methods/results.json), and [skill checks](evidence/skill-validation.json) record the scope. Raw trial paths/PIDs identify their original local runs; use new output paths to replay.

## Guidance and format choices

Bootstrap, Adversarial Cases, Cross-Examine and Hill Climb reference the shared generation/failure/data recipes. Only Markdown was added to the skill folders. Consumers adapt methods to their own native task and runner; no experiment runtime or SDK is copied with these references.

The README now centers eval-driven development, diagrams the observation route through the existing expert-mode command, and distinguishes untuned, synthetic injection, adversarial and true labeled evidence. LangChain's eval-engineering is referenced for production-trace task engineering, without vendoring or invoking its workflow. Harbor is preferred for new executable agent tasks, with established or owner-selected formats supported. The playground preserves its existing native runner; no Harbor runtime, container execution or format migration was performed.

Explicit enumeration suffices for this small action vocabulary. Hypothesis is conditional; Z3 and a network proxy lack a justified boundary here. Native state is directly checkable, so semantic judges are deferred. These exposed synthetic/adversarial checks establish no human labels, held-out improvement, production prevalence, power-loss durability or security containment. No framework installation is required by a skill.
