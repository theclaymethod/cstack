# Results

Each version ran once in a fresh gpt-6-astra session with a blank index and the same operator policy. Four interview rounds were available before wrap-up. The operator disclosed the concern only when the interviewer asked a qualifying question.

| Version | Question that elicited the concern | Immediate Undo preserved | Edited line preserved in final index | Rejoin in final index |
| --- | --- | --- | --- | --- |
| [Original 9a65d68](evidence/original/dialogue.json) | Missed in four rounds | Yes | Missing | Never raised |
| [Previously published 293753c](evidence/published/dialogue.json) | Missed in four rounds | Yes | Missing | Never raised |
| [Revised skill](evidence/candidate/dialogue.json) | First question, asking what happened or worried the developer | Yes | Yes | Explicitly deferred |

All three respected the answers they received. No developer had to re-answer a settled question. The original asked for scope confirmation in its fourth round. The prior published run spent its remaining rounds on remote visibility, multiple strokes and the empty-history control. Those were plausible questions but none exposed the motivating concern.

Compare the revised [opening index](evidence/candidate/turn-1.md) with its [final index](evidence/candidate/turn-2.md). The immediate Undo row is identical. The new rows cover ownership of separate lines and preservation of another person's edit to the same line. The latter keeps the moved endpoint in its new position. Leaving and returning has no pass/fail outcome.

The existing correction replay also passed both branches with this revision. Only B changed from notify to silent in [one date](evidence/regression-one-date/result.json). Only C changed from silent to notify in [whole series](evidence/regression-series/result.json). D stayed open in both.

The revision was selected after inspecting the two misses. This is a regression case for that failure and one observation per version, not a held-out estimate of interview quality.

## Conditional opening question

The [first wording](evidence/conditional/dialogue.json) found the hidden concern in round two by asking about someone moving the same mark. It began by proposing ownership semantics. We tightened the instruction to distinguish an opening that gives only ordinary behavior from one that supplies an incident.

The [shipped wording](evidence/conditional-final/dialogue.json) asked for the motivating concern in round one and waited. Its [final index](evidence/conditional-final/turn-2.md) retains immediate Undo, distinguishes separate marks from another person's edit to the same mark, and leaves rejoining open. No settled question was repeated. Both existing correction branches also passed with this wording. Only the corrected row changed in [one date](../correction/results/conditional-final/one-date/result.json) and [whole series](../correction/results/conditional-final/series/result.json).
