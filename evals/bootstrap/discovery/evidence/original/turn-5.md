# Shared whiteboard undo

## Product brief

A person drawing on the shared whiteboard can undo their own mark. The first two scenarios describe what that person sees after drawing one line and selecting Undo. The decisions below establish the expectations. Neither scenario has a runnable evaluator or an observed execution result.

## Drawing and undoing a line

| Scenario | Situation | Expected result on Alice’s board | Why it matters |
| --- | --- | --- | --- |
| WB-01 · r1 | Alice draws one line and immediately selects Undo. | Her line disappears. | Establishes the ordinary single-line undo. |
| WB-02 · r1 | Alice draws a red line. Bob draws a blue line. Alice sees both and selects Undo. | Alice’s red line disappears. Bob’s blue line stays. | Bob drawing last must not cause Alice’s Undo to remove his line. |

### Decision history and coverage

- **WB-01 r1** reflects the owner’s starting requirement, “When I draw a line and immediately undo, it disappears.” The README gives the same example.
- **WB-02 r1** applies the owner’s answer to the two-person example, “My undo applies to my marks only.”
- Both expectations come from owner decisions. The owner has not separately reviewed these scenario revisions or labeled any product output. No suite or case IDs are mapped.

## Deferred decisions

- **Stroke grouping.** If a rectangle consists of four separately drawn sides, how much does one Undo remove?
- **Undo order.** When a person has several marks, which mark or group does each successive Undo remove?
- **Collaborator visibility.** When Alice undoes a line, when does Bob see it disappear? Whether Bob needs to refresh remains open.

The owner explicitly left these questions undecided. They supply no pass or fail criteria for either scenario.
