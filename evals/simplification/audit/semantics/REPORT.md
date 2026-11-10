# Independent semantics attack: bounded clean result

No confirmed discrepancy between the frozen intent, skill guidance and native outcomes in these probes. No canonical repair is proposed. This is finite fixture evidence, not production validation or a proof of global correctness.

## Source, scope and access

Read the parent `INTENT.md`, frozen `/ablation`, `/bitter-lesson`, and adversarial-case construction instructions. Materialized this disposable workspace with the frozen `new_workspace.py`. Never edited frozen source, grader, canonical cases, adapter, model stand-ins, or another role's workspace. Used public `Experiment` operations and standalone candidate variants; no experiment-object manipulation, operator fault injection, model calls, network access or dependency installation. Source hashes before/after and matches to the frozen checkout are in `semantics-evidence/source-identity-*.json` and `frozen-source-matches.json` (13 source files matched).

All expectations are synthetic and source-backed by the written fixture contract. Additional metadata cases are separately constructed inputs, outside canonical case membership. Candidates receive only request/state, plus their compiled prompt/model source; these candidates do not read expected labels or evaluator files at runtime.

## Executed challenges and outcomes

Executed **180 native cases across 25 attempts**: 96 development cases, 24 frozen confirmation cases and 60 standalone representation/state-control cases. No failed setup, interrupted execution or omitted native attempt. Both native ledgers retain exact membership and counts; raw output, resulting state, native verdict, candidate snapshots and source manifests remain under each run directory.

| Hypothesis / condition | Actual native observation | Adjudication proposal |
| --- | --- | --- |
| Individually safe duplicate deletions might be combined without detection | Each deletion passes 8/8; deleting both fails `dev-duplicate` (7/8), rejected relative to fixed original | Known interaction correctly detected |
| Single-removal failures might hide a valid joint deletion | Each single conflict deletion passes 4/8; removing both passes 8/8 | Valid combined solution accepted |
| Search might privilege one equivalent duplicate reminder | Old lean A and old lean B each pass 8/8 development and 4/4 confirmation | Both valid alternatives accepted |
| Migration might use incompatible simplified designs or hide loss | Same retained units `contract, duplicate-b` in both rows; full old/new each 4/4 confirmation, simplified old 2/4, simplified new 4/4 | Proposed bundle passes original and new-existing gates; old simplification correctly fails |
| Reference ticket IDs or action wording might be overrequired | Alternate unique `independent-*` IDs, `clarify` for duplicate cases and extra new-ticket metadata pass all 12 canonical cases | Legitimate representations accepted |
| Metadata might be lost or a JSON type change tolerated | Prior nested metadata/extra ticket fields preserved: base and alternative each 4/4; Boolean-to-number mutation rejected 0/4 | State semantics preserved on these probes |
| Wrong state, duplicate IDs or output shape might pass | Added state field rejected 0/12; duplicate-ID control fails both collision cases; extra top-level output field yields ERROR on all 12 | Incorrect outcomes rejected and errors retained |

The migration scores are programmed stand-in behavior. The confirmation matrix interaction is 0.5 on this finite pass-fraction scale; it measures this controlled fixture only. It does not establish an empirical model improvement, causal production effect, token savings, cost savings or latency savings.

## Independent witnesses and replay

`semantics-evidence/independent-witnesses.json` inspects 16 actual valid-output traces independently of their native verdict fields: prior state/record preservation, unique alternate IDs, allowed duplicate action and appended metadata. It also independently records observed wrong state changes, duplicate IDs and Boolean-to-number mutation. `inspect_evidence.py` performs those inspections without native execution.

Reproduce in a fresh materialized workspace, copying these two scripts into its `eval-runs/` directory:

```sh
python3 eval-runs/reproduce_semantics.py
python3 eval-runs/inspect_evidence.py
```

The first refuses to overwrite its existing evidence directory. `reproduce_semantics.py` is the complete bounded driver; `semantics-evidence/results.json` retains every comparison and all candidate outcomes. `adapter/native/executions.json` records 120 case executions; `native-representation-controls/executions.json` records 60. All 25 attempts and unrepaired negative outputs are retained. There was no reduction search after these receipts.

## Remaining hypotheses / limits

No unconfirmed defect is promoted as a finding. Hostile filesystem access, unusual public-API lifecycle/operator mutations and broader arbitrary input-language coverage were not tested by this role. The complete task algorithm remains embedded in these deterministic stand-ins, as disclosed by the adapter. Confirmation inputs are readable; this audit establishes bounded mechanics and observed native decisions only.
