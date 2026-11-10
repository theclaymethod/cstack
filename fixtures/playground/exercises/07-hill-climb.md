# Hill Climb: improve the support agent

Begin with the deliberately flawed `support_agent.py`. For an independent attempt, inspect actual failures before reading the supplied candidate solutions. The examples are development controls once opened.

Handoff:

> Use Hill Climb to improve support_agent.py against this project's eval. Only support_agent.py is editable; keep the runner, synthetic spec, core cases, and rubric fixed. Reuse evaluate.py's native campaign commands. This deterministic exercise's objective is a higher development pass rate with zero regressions of previously passing cases, followed by the declared baseline/candidate confirmation comparison. The budget is 48 case attempts including baseline, failures, and confirmation, with 8 case attempts reserved for confirmation. No provider/model calls or paid tools are needed. Run actual changed candidates, preserve the best measured artifact after failed proposals, and deliver its diff and evidence. Treat all supplied cases as synthetic and report actual exposure rather than claiming unseen generalization.

Try an unsuccessful final proposal after finding a good candidate. Confirm that it does not replace the measured incumbent. For the no-improvement path, start a fresh campaign and submit an unchanged copy of the baseline. For a search-budget stop, start with `--max-case-runs 16 --reserve-case-runs 8`; the eight-case baseline leaves no search allocation.

Resume the same campaign with `status` and `verify`. An authorized change to the evaluator or cases requires a new campaign and baseline; it is not another target candidate.

Completion: candidate snapshots actually executed, attributed hypotheses, per-case changes, regression gates, charged attempts, confirmation status, selected artifact and patch, and an explicit stopping reason. Honest no-improvement and budget-stop results are normal outcomes.
