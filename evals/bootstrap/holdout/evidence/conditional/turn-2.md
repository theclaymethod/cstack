# Kanban welcome demo

After the video change, a person who starts the demo on the Kanban welcome screen must see moving video in both VS Code and JetBrains.

| ID | Starting situation | Required observable outcome | Reported result in the new build |
| --- | --- | --- | --- |
| KW-01 | Open the Kanban welcome screen in VS Code and start the updated demo. | The demo plays in the welcome screen, with visible motion as playback progresses. | Fails. The player shows a still frame. |
| KW-02 | Open the Kanban welcome screen in JetBrains and start the updated demo. | The demo plays in the welcome screen, with visible motion as playback progresses. | Passes. The demo plays where the player previously appeared blank. |

Both scenarios must pass in the build that ships. KW-01 currently blocks release.

**Deferred boundary.** The expected experience on an unsupported host is undecided.
