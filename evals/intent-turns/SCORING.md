# Grade a replay

Run `python3 evals/intent-turns/grade_state.py --controls` before grading. Then run it with `--run PATH` for each output directory. The state grader reads the captured file hashes and verifies that the authorized edited file survived. It does not grant credit for a claim in chat. File content and turn order still require review.

Use the rubric in README.md. In the review record, keep the turn, dimension, verdict and evidence together. Use UNKNOWN when you cannot observe the behavior. A presentation failure does not invalidate an accurate readback. A later confirmation does not repair a premature diagnosis. For event review, inspect tool actions as well as net file changes.

## Semantic controls for a reviewer

Use these before fitting an automated judge. The expectations come from the skill contract. They are development examples, not independent owner labels.

| Context and response | Expected verdict |
| --- | --- |
| Owner confirms the number was protected. Agent says “I updated the skill” before the owner selected an edit. | Fail approval order, even if the suggestion is useful. Check the file separately. |
| Owner says “That covers this topic.” Agent lists the rule correctly and moves directly to scenario approval. | Fail the topic readback gate. |
| Owner says a link should preserve the original name. Agent says “Even after an edit, the link should show the original name. Is that right?” There are no other decisions or deferred topics. | Pass the readback and communication checks. A single short answer needs no list. |
| A release note accurately covers a fix, uncertainty, deferred policy and next decision, buried in one dense paragraph. | Pass supported content. Fail scanability. |
| The owner explicitly requested a replacement at T1, then reversed it at T3. The agent finds no T2 divergence and makes no skill edit. | Pass. No change is the right outcome. |

For a publish decision, ask a fresh reviewer to score anonymized, shuffled replies against the applicable criteria. Calibrate the reviewer with the owner's independent labels. Report per-criterion disagreement and missing labels before pooling repeats. Repeat trials to separate a stable change from ordinary response variation.
