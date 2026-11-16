# Kanban welcome demo

The updated demo must play moving video in the Kanban welcome view in both VS Code and JetBrains.

| ID | Starting situation | Required observable outcome | Developer-reported result |
| --- | --- | --- | --- |
| KAN-001 | A VS Code user opens the welcome view and starts the updated demo. | The video advances and the user sees the board actions unfold inside VS Code. | Fails. The player shows a still frame. |
| KAN-002 | A JetBrains user opens the welcome view and starts the updated demo. | The video advances and the user sees the board actions unfold inside JetBrains. | Passes. The demo plays. |

The VS Code regression blocks shipping this build. JetBrains meets the same playback requirement.

**Open boundary.** The expected behavior on an unsupported host is undecided.
