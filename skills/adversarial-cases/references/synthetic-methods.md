# Choose a synthetic generation method

Use project evidence and its native case schema. Implement any needed generator in the consuming project. These recipes require no C Stack runtime, fixture, or shared dependency.

| Gap | Method | Evidence that earns adoption |
| --- | --- | --- |
| A decision changes with one fact | Render minimal contrasts from structured conditions | Both conditions are feasible; the changed fact explains the expectation. |
| Correctness depends on earlier effects | Generate reachable action sequences with an independent transition model | Each successor uses a checked actual predecessor; preserve the first failure and stop invalid continuations. |
| A failure is obscured by context | Remove whole records or steps, then finer fields | The same requirement fails, applicability remains, and legitimate controls still pass. Retain rejected reductions. |
| Many generated cases repeat coverage | Compare cases against reviewed requirement-linked faulty variants | List defects detected, survivors, errors, equivalent/invalid variants and executions. Select a small corpus while retaining useful boundaries. |
| Intertwined constraints defeat simple enumeration | Consider a bounded solver such as Z3 | Compare with independent enumeration on a small domain. Satisfiability establishes the encoded constraints, not realism. Keep unknown unresolved. |
| A semantic judge needs calibration | Construct independently verified output contrasts | Judge accepts legitimate alternatives and rejects targeted faults. Model agreement does not supply expert truth. |

## Generate conditions before text

Start from the original requirement, supported operations, identities, permissions and reachable state. Render requests only after those facts and their proposed expected behavior agree. Existing project builders or a short deterministic enumerator often suffice. Hypothesis rules, bundles and preconditions become useful when the action vocabulary grows; they do not supply the correct state model.

Record generator/source identity, construction method, ancestry and applicability with each case. For stateful programs, run each candidate from a fresh initial state. Advance using its actual output only after the native checker validates the step. An error or broken invariant ends that valid prefix. Candidate-specific reachable states can become new cases when independently checked against the original contract and legitimate controls. Preserve legitimate metadata and output representations.

## Shrink and select on behavior

Use the real runner and a bounded predicate that distinguishes the same defect from a crash, setup error or different failure. Recheck positive controls after each retained reduction. A bounded structured reduction is not automatically globally smallest or even 1-minimal. Record the tested deletions, unresolved trials and stopping reason.

Freeze the fault catalog before comparing it with seeds. Compare under a declared execution ceiling, report actual calls for each arm, and separate invalid execution from behavioral detection. Equal detection vectors only nominate redundancy for review. A newly detected declared synthetic fault establishes that narrow gain; it does not estimate production coverage or generalization.

Group connected source/construction ancestry, transformations, reductions and exact duplicate inputs into the same partition. Repeatedly used validation is adaptive development evidence. Neither new seeds nor renamed splits restore independence. Keep model-proposed expectations pending under Bootstrap's authority; explicit fixture-contract labels remain synthetic and are not human judgments.

For DSPy use the [data handoff](../../hill-climb/references/data-handoff.md). Execution errors and operator-only fault receipts need their own reporting; they are not automatically training labels.

The C Stack checkout validates these recipes in `fixtures/playground/methods`. It uses explicit enumeration, structured record/step reduction and a frozen fault catalog. Consumers adapt the recipe to their project rather than depend on that demonstration.

Sources: [Hypothesis stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html), [delta debugging](https://www.st.cs.uni-saarland.de/publications/files/zeller-tse-2002.pdf), [mutation testing](https://pitest.org/), [Z3 guide](https://microsoft.github.io/z3guide/programming/Z3%20Python/Introduction/).
