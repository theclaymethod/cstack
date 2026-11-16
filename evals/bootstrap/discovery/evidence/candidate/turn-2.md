# Undo on the shared whiteboard

My Undo applies only to my own marks. If someone else edits a line I drew before I choose Undo, the line stays exactly as they edited it.

| Scenario | Starting situation | Action | Observable outcome |
| --- | --- | --- | --- |
| UNDO-001 | I have just drawn a line and can see it on the board. | I immediately choose Undo. | The line disappears from my view of the board. |
| UNDO-002 | I drew a red line. Someone else then drew a separate blue line. Neither line has been edited. | I choose Undo. | My red line disappears. Their blue line stays as drawn. |
| UNDO-003 | I drew a line. Someone else then moved one endpoint. | I choose Undo. | The line stays exactly as they left it, with the endpoint in its new position. |

## Deferred

Whether I can undo a mark from a previous visit after I leave the board and return is undecided.
