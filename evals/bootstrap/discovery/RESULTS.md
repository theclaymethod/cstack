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
