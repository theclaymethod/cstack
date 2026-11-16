# Shared whiteboard undo

## Drawing and undoing a line

The owner and the project README describe one outcome. When a person draws a line and immediately selects Undo, the line disappears. This is the starting requirement. The directory contains no implementation, examples beyond the README, or executable checks.

## Owner decisions

When asked whose drawing Undo affects after two people take turns, the owner specified, “My undo applies to my marks only.” If Alice draws a red line, Bob draws a blue line, and Alice selects Undo, Alice’s red line disappears and Bob’s blue line stays.

## Open decision

If Alice draws two separate lines, how many should one Undo remove, and in what order should repeated undos remove them? The product brief and scenario index are still in discovery.
