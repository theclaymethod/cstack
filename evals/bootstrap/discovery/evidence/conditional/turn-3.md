# Shared whiteboard undo

While you stay on the board, your Undo applies only to your own marks. If someone has since edited a line you drew, Undo leaves the line exactly as they edited it.

| ID | Starting situation and action | Observable outcome |
| --- | --- | --- |
| UNDO-001 | You draw a line, then immediately press Undo. | The line disappears from your view. |
| UNDO-002 | You draw a blue line. Sam draws a separate red line. You see both, then press Undo. | Your blue line disappears from your view. Sam’s red line stays visible. |
| UNDO-003 | You draw a blue line. Sam moves it. You see the line in its new position, then press Undo. | The blue line stays exactly where Sam put it, with its appearance intact. |
| UNDO-004 | You draw a line, leave the board, return, and try to undo the drawing. | Deferred. Whether you can still undo a mark from your previous visit is undecided. |
