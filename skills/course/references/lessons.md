# Exercises 01–13

Teach these in order. Each block names the evidence to put beside the claim, the one question to ask, a hint that points at that evidence, and the checkpoint that must already be true before you mark the exercise complete. Commands run from the materialized playground. Paths are relative to that workspace.

The handoff paragraphs in `exercises/` are requests to the coding agent. Use the named skill for that work. Keep the teaching turn anyway: show the evidence, ask one question, wait, checkpoint. Do not read the whole exercise aloud.

| Exercise | Skill in use | Where the work goes |
| --- | --- | --- |
| 01 Expert Mode | expert-mode | `eval-runs/expert-baseline` and a review record |
| 02 Distill Me | distill-me | the same review records, merged twice |
| 03 Bootstrap | bootstrap | `eval-runs/password-bootstrap` |
| 04 Create Eval | create-eval | `evals/generated/` and a grader run |
| 05 Run Eval | run-eval | `eval-runs/run-baseline` and `eval-runs/run-regression` |
| 06 Cross-Examine | cross-examine | `eval-runs/claim-audit` |
| 07 Hill Climb | hill-climb | a campaign directory under `eval-runs/` |
| 08 Adversarial Cases | adversarial-cases | `eval-runs/case-build` |
| 09 Methods | adversarial-cases and hill-climb references | `eval-runs/methods` |
| 10 Calibrate Judge | calibrate-judge | a fresh `eval-runs/` judge directory |
| 11 Ablation | ablation | a fresh `eval-runs/` simplification directory |
| 12 Bitter Lesson | bitter-lesson, using ablation | a fresh `eval-runs/` comparison |
| 13 Review capture | expert-mode calibration-capture reference | `eval-runs/` capture records |

## 01 · Expert Mode

Evidence: run `python3 evaluate.py run --candidate support_agent.py --suite development --out eval-runs/expert-baseline`. Open the how-to case in `evals/cases.jsonl` and the matching object in `eval-runs/expert-baseline/traces.jsonl`. Say this is a synthetic fixture run. The suggested sentence in `exercises/01-expert-mode.md` is an example, not their judgment.

Question: “For this how-to output, what should have happened, and which field in the trace shows that it did not?”

Wait. Save their words. If they also name an uncertainty, keep it unresolved rather than turning it into a second label.

Hint: point at that trace’s `output.action` and the ticket list. Do not say which action is right.

Checkpoint: a capture record quotes them, names the output version, and states a criterion. The uncertainty is still uncertain. `support_agent.py` is unchanged. The baseline receipt is in `artifacts`.

## 02 · Distill Me

Evidence: the exercise 01 record, then the same extraction run a second time. If they did not do 01 in this session, use `exercises/fixtures/review-session.md` and say those lines are scripted source, not a live expert and not human gold.

Question: “After the second merge, which record stayed a single example, and which statement is still not a judgment?”

Hint: point at the two saved lines that share a source and an output version, and at the sentence that was only a suggestion.

Checkpoint: the resolved example was not duplicated, earlier history is still there, and an agent suggestion was not promoted into their judgment. Scripted source stays labeled scripted.

## 03 · Bootstrap

Evidence: `evals/spec.json` says what the current fixture covers. Password reset is not in that contract. Interview in short rounds. Show scenario cards with stable ids, the situation, the guessed behavior, and the reason. Guesses are not gold.

Question: “Which of these cards do you approve as written, which one do you correct, and which one do you defer?”

Ask that only after the cards exist. Leave at least one boundary unresolved if they are willing.

Hint: point at one card’s guessed action and at the current spec’s preserved VPN behavior. Do not approve a card for them.

Checkpoint: `eval-runs/password-bootstrap` has a versioned approved handoff, the correction history, and an explicit pending queue. Unreviewed cards are not in the authoring set. Their decisions are separate from the prewritten spec.

## 04 · Create Eval

Evidence: one approved card from exercise 03, or one captured judgment from exercise 01, beside `evals/cases.jsonl` so they can see the native fields (`id`, `suite`, `family`, `request`, `state`, `expected`).

Question: “Which field in this case is fixed by the decision you already made, and which part is still only a proposal?”

Wait before writing the case. Then show the case and the actual grader control output together.

Hint: point at their approved sentence and at the case’s `expected` object. Do not treat a written expectation as a label on a generated output.

Checkpoint: approved cases live under `evals/generated/`, pending cases are listed separately, and legitimate and failing controls ran through `evaluate.py`. Source ids trace back to the approved card or capture. The core suite was not rewritten.

## 05 · Run Eval

Evidence: run the three commands in `exercises/05-run-eval.md`. Put the baseline summary beside the regression summary, and open one trace that changed.

Question: “The regression candidate’s aggregate is higher. Which previously passing case is no longer passing, and where is that in the comparison?”

Hint: point at `evaluate.py compare` output, or at the two traces for that case id. Do not interpret the higher aggregate as permission to replace `support_agent.py`.

Checkpoint: both receipts exist, selected ids and candidate hashes are recorded, ERROR and FAIL are separate, and the comparison names the regression. These checks are not semantic-judge calibration.

## 06 · Cross-Examine

Evidence: run `python3 exercises/fixtures/verify_claim.py exercises/fixtures/forged-result.json`. Show the forged claim beside the ticket state it ignores. Say `verify_claim.py` is the defective exercise artifact. `evaluate.py` is the native grader.

Question: “What did this verifier treat as success, and which part of the resulting state did it not look at?”

After they answer, reproduce, repair under `eval-runs/claim-audit`, and replay the forged and legitimate outcomes. If attacker, defender, and a fresh reviewer are not separate sessions, record the audit as unreviewed rather than independent.

Hint: point at the claimed action in the JSON and at the ticket list the script does not read.

Checkpoint: the ledger distinguishes the hypothesis, the observed state, and any independent acceptance. The original `verify_claim.py` is unchanged. A repair was replayed against the forged case and a legitimate alternative. No new flaw is claimed in `evaluate.py`.

## 07 · Hill Climb

Evidence: the baseline receipt’s failing case ids, before any example candidate is opened. `examples/candidates/` become exposed development material once read.

Question: “Which failing case are you trying to change, and which passing case must stay passing?”

Use a new campaign directory. The budget and reserve in the exercise are this exercise’s policy. Edit only `support_agent.py` if they are applying a change to the live file; otherwise deliver `best.py` and `best.diff` and leave the live file alone when it has unrelated edits. Show a rejected higher-scoring candidate beside the incumbent it did not replace.

Hint: point at one failing trace and one passing trace. Do not name the example candidate’s patch.

Checkpoint: attempts have hypotheses and executed snapshots, regressions are visible, the reserve was charged as reserved, and the stop reason is explicit. A no-improvement result counts. Changing the evaluator would be a new campaign, and it was not done here.

## 08 · Adversarial Cases

Evidence: one requirement from `evals/spec.json` and one real run through `evaluate.py`. The parent still owns approval. This exercise practices construction.

Question: “What would you change in the setup so this requirement is actually stressed, and what unchanged run is the control?”

Build under `eval-runs/case-build`. Keep the canonical runner, spec, cases, and rubric fixed. Bound the work to the exercise’s case and interruption limits.

Hint: point at the field the requirement constrains and at the control run’s matching field. A configured fault name is not activation.

Checkpoint: the handoff separates armed, activated, and outcome, or it says not activated. Clean and legitimate-alternative controls are present. Guesses for Bootstrap are still pending. Nothing is marked as an adjudicated defect. Operator access is labeled as operator access.

## 09 · Methods and DSPy

Evidence: `python3 -m methods.run --out eval-runs/methods`. Open the reachable-sequence result, one reduction that preserved it, one control that rejected a shortcut, and one fault record. Say the optional DSPy SDK check did not run unless `--dspy-check` was actually used.

Question: “Which recorded event shows the fault happened, and which neighboring record shows a trigger that never fired?”

Hint: point at the activation witness and at the unreachable kill trigger. Do not treat the process exit code as the name of the fault.

Checkpoint: they can distinguish a configured trigger, an observed event, a perturbation, and surviving state. Proposed labels were not exported as gold. Expected criteria are not in the model inputs. The original spec, cases, rubric, and evaluator are unchanged.

## 10 · Calibrate Judge

Evidence: `python3 -m judge_calibration.run --out eval-runs/judge-calibration` (or a fresh directory if that one exists). Open the baseline comparison and one normalized verdict beside the native outcome. Say both judge backends are deterministic stand-ins. The labels are code-derived, not human gold.

Question: “This selected policy matches the native outcome on the row in front of you. What did the judge actually see, and what was kept out of its input?”

Hint: point at the projected input and at the label file that is not in that projection. Concentration is not a probability of failure.

Checkpoint: final predictions were frozen before the final comparison. A false pass or false rejection is described if one is in the report, and agreement is not invented if the report does not show it. Live model calibration is still unverified. The core runner and cases were not edited.

## 11 · Ablation

Evidence: the full `old-fixture` prompt text beside the original baseline’s native result. Run the simplification adapter the exercise names, into a new `eval-runs/` directory. Show one deletion that was executed and one combination, not only the selected score.

Question: “Which removed piece is still absent in the candidate you are looking at, and which baseline result is the quality bar for that candidate?”

Hint: point at the retained-set diff and at the original baseline row. A budget stop is not proof that nothing smaller exists.

Checkpoint: combined deletions were executed, invalid candidates are distinct from task failures, the quality bar is the original baseline, and the selected artifact is recoverable. No provider call was made. The model stand-in stayed fixed.

## 12 · Bitter Lesson

Evidence: the comparison matrix from the exercise’s adapter run. Show the old stand-in and the new stand-in with the same simplified prompt, plus each stand-in with the existing prompt. Say these model names are programmed stand-ins.

Question: “Which cell would you need before you could say the simpler prompt held up on both stand-ins, and is that cell in this output?”

Hint: point at the two simplified cells and at any missing one. A gain on the new stand-in does not hide a regression in another cell.

Checkpoint: the four final cells are either measured or explicitly missing. The simplified text is the same text in both model rows. No deployment was performed. The result is scoped to the synthetic adapter.

## 13 · Review capture

Evidence: one false ticket-creation claim and one legitimate alternative, executed through `evaluate.py`, with input, output, and state preserved. Then show the four scripted signals in `exercises/13-review-calibration-capture.md` and say they are fixture roles.

Question: “Which of these four signals is a judgment of a specific output, and which one has not been labeled by the scripted reviewer?”

The parent offers a scoped save. It does not write labels before consent. Builders do not ask a competing question. Accepting capture for this review does not turn on ongoing Expert Mode.

Hint: point at the trace that shows whether a ticket was created, and at the signal that never names an output.

Checkpoint: consent, eligible rows, and excluded rows are separate. A repeated decision did not duplicate the row. A retraction is append-only. Verdicts and quotes are outside the judge input preview. A later tamper of a saved snapshot is rejected when they run that check, and the untampered capture remains. No fitting or upload was authorized.

## Handoff

After 13, ask them to finish, in their words: “I checked ___. The run ___ showed ___. That does not yet show ___. The next test I want is ___.” Write `eval-runs/course/progress/handoff.md` from that answer. One part at a time is fine. Do not fill in the blanks for them.
