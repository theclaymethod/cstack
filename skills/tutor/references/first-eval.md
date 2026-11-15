# Choose a behavior and check it

Start from a feature promise: “Support can explain how to connect or open a ticket when asked.” The learner needs no prior runs, traces or implementation. Supply this example if they have no project ready. Their first trace will come from the exercise. With an unbuilt product, label the checked result as a playground demonstration and keep their own product execution marked unrun. Allow 45–55 minutes including a retry. The learner chooses the behavior; the tutor handles commands, case syntax, and receipts.

## Choose the slice · 5 minutes

In a real project, inspect existing suites, assertions, and run commands. Ask which product decision needs evidence first. Offer a concrete contrast: “Should we check whether support opened the right ticket, or whether its troubleshooting advice was accurate?” Either is a plausible suite. Work on one this sitting. In a project with an existing suite, show one covered behavior and one gap. With no evals, offer one ordinary scenario and its nearest contrast. Keep other suite ideas under “later.”

For the prepared lesson, use CStack's synthetic VPN playground. Run its scripts/new_workspace.py with --out pointing to a fresh workspace, or reuse the learner's materialized workspace. Put new files in eval-runs/tutor-first-eval/. For the empty-start practice begin with no cases in this new exercise folder. For the existing-suite practice seed it with the native dev-explicit row from evals/cases.jsonl. Tell the learner this is a practice subset. Leave the shipped suites intact.

## Review the scenario · 10 minutes

Show “Please open a ticket for my VPN problem” beside “How do I connect to the VPN?” Both start with one known account and no tickets. Work the explicit request aloud: creating one ticket is the requested action. Ask: “What should the agent do for the how-to request?” Wait. If needed, point at the words that distinguish guidance from authorization to act.

Draft SCENARIOS.md in the exercise folder. Show the situation and proposed observable outcome in plain language. Use distinct stable IDs for explicit action and guidance only. On the existing-suite path link the explicit-action entry to dev-explicit and show its assertion. On either path ask the learner to approve, correct or defer the proposed expectations. Only approved revisions move into case authoring. Record which suite checks which criterion. Advice quality can remain a separate future suite even when it would use the same request.

## Run the check · 10 minutes

For the playground, use dev-howto and dev-explicit as native row templates. Translate the approved decisions into development rows in a separate cases.jsonl. Keep an existing row if it already checks the decision. Link scenario ID and revision to the suite and case IDs in the index. If the learner chose a policy the grader cannot express, explain the limit before proceeding. In their own project, use its native runner instead.

From the materialized playground, run the following with the exercise case file. Choose a fresh output directory on each run.

```sh
python3 evaluate.py run --candidate support_agent.py --suite development \
  --cases eval-runs/tutor-first-eval/cases.jsonl --out eval-runs/tutor-first-eval/run-01
```

Show the how-to request, approved rule, and resulting ticket list from traces.jsonl together. Ask which observation settles the case. With the shipped agent, the explicit-ticket case passes and the how-to case fails because a ticket was created. Separate runner errors from verdicts. A routing pass gives no evidence about the quality of troubleshooting advice.

## Interpret fresh evidence · 10 minutes plus retry

Make a fresh development case under the approved guidance scenario: “Where can I find the VPN setup instructions?” Keep the account and initial state fixed. Run it; show the request and actual action and ticket list before showing the grader's verdict. Ask: “Does this meet the approved rule, and what in the trace settles it?” Accept an equivalent explanation grounded in the effect. Then show the receipt.

If the learner needs help, point to the before/after ticket count. If they want the answer, explain it and record that attempt as worked. For a fresh independent attempt change the request to “Please create a ticket for this VPN outage” under the approved explicit-action scenario. Both worked and hinted attempts need fresh evidence before counting as independent. If time runs out, preserve partial progress.

## Choose the next workflow · 5 minutes

Teach the choices first. Use /bootstrap when the expected behavior is still open, /cross-examine when a grader might accept a wrong result, and /hill-climb when the check is trusted and the agent fails it. Keep this three-choice key visible. Work one example: if nobody has decided what to do for two matching accounts, use /bootstrap to settle that boundary.

Now give a fresh situation: “The response says a ticket was opened. The grader passes it. The ticket list is empty.” Ask which workflow they would use and what evidence led them there. Wait. Look for challenging the grader that accepted the unsupported claim. Accept the reasoning in ordinary language. If they need a hint or the worked answer, use a different situation for the independent retry: “The grader correctly flags an unwanted ticket on each run. You have approval to improve the agent against this fixed suite.” Look for /hill-climb. Record their choice and reason; running a second workflow is outside this sitting.

## Finish or resume · 5 minutes

After a decision, update progress.md beside the index with the chosen suite, scenario revisions, cases seen, learner's own words, assistance level, receipt paths, and the exact pending question. On resume inspect the referenced evidence and ask that question. Finish when the learner has approved a scenario, run a real check with the tutor, independently explained a fresh verdict, and then independently selected a suitable next workflow with a reason. Leave them the index and receipt that support their conclusion.

At the first sitting’s handoff, tell the learner what to bring back: one real request where the product did something they would change, and the evidence showing what happened. They can finish this sitting before their product has any traces.

## Review a real failure

On a return visit, show one actual request beside its observed outcome. Ask “What should have happened here?” Wait for the learner’s judgment. Find the closest approved scenario in SCENARIOS.md and inspect what its grader checks. If possible, replay the observed failure against that check.

For example, suppose a trace shows a second open ticket for the same outage. If the suite only covers opening a first ticket, propose a case that starts with an open ticket and checks the resulting ticket count. If the existing duplicate-ticket case already catches the failure, link the trace to that case and investigate the agent. If that case passes despite the duplicate, inspect the grader. This is a worked example; use the learner’s trace for the actual decision.

For several failures, group those with the same underlying behavior. Ask which gap matters most, using impact and recurrence where the traces support them. Record the chosen failure, trace reference, and coverage decision in the index. Derive a regression case from the approved expectation and run it against the failing behavior. If replay is unavailable, record what still needs checking.
