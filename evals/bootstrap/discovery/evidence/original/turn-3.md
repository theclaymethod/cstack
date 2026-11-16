# Shared whiteboard undo

## Drawing and undoing a line

The owner and the project README describe one outcome. When a person draws a line and immediately selects Undo, the line disappears. This is the starting requirement. The directory contains no implementation, examples beyond the README, or executable checks.

## Owner decisions

When asked whose drawing Undo affects after two people take turns, the owner specified, “My undo applies to my marks only.” If Alice draws a red line, Bob draws a blue line, and Alice selects Undo, Alice’s red line disappears and Bob’s blue line stays.

## Deferred decision

The owner said there is no decision yet on how strokes are grouped or which of several marks Undo removes first. Neither behavior has an approved expectation.

## Open decision

When Alice undoes her only line while Bob is watching the same board, when should Bob see it disappear?
