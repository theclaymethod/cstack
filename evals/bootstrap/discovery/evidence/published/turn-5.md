# Shared whiteboard undo

My Undo applies only to my marks. If I draw one line and press Undo, that line disappears from my view, even if someone else has drawn a line since.

| ID | Starting situation and action | Agreed outcome | Deferred decision |
| --- | --- | --- | --- |
| UNDO-001 | I draw a blue line on an empty board and immediately press Undo. | I see an empty board. | — |
| UNDO-002 | I draw a blue line. Sam draws a red line. I see both and press Undo. | My blue line disappears. Sam’s red line stays visible. | — |
| UNDO-003 | Sam and I both see my blue line and Sam’s red line. I press Undo while Sam watches. | I see only Sam’s red line. | What Sam sees after my Undo. |
| UNDO-004 | On an empty board, I draw a blue line, lift the pen, draw a green line, and press Undo once. | — | Which of my two lines remain after one Undo. |
| UNDO-005 | I join a board with Sam’s red line, have drawn nothing, and try to use Undo. | Sam’s red line stays visible. | How the interface handles Undo when I have nothing to undo. |
