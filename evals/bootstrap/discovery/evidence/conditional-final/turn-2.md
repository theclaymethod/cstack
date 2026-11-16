# Shared whiteboard undo

While I’m on the board, Undo applies only to my marks. If someone else has edited my line, Undo preserves the line exactly as they edited it.

| ID | Starting situation | Action | Observable outcome |
| --- | --- | --- | --- |
| UNDO-001 | I have just drawn one line on the board. | I immediately choose Undo. | My line disappears from the board. |
| UNDO-002 | I draw a line, then someone else draws a separate line. | I choose Undo. | My line disappears. Their line stays exactly as drawn. |
| UNDO-003 | I draw one line, then someone else moves its endpoint. | I choose Undo. | The line stays on the board exactly as they edited it, with the endpoint where they placed it. |

## Open boundary

| ID | Starting situation | Action | Observable outcome |
| --- | --- | --- | --- |
| UNDO-004 | I draw a line, leave the board, and return. | I choose Undo. | Deferred. Whether I can undo a mark from before I left is undecided. |
