# Kanban welcome demo

After the video change, a person opening the Kanban welcome screen in either JetBrains or VS Code must be able to watch the demo play as moving video.

| ID | Starting situation | Required observable outcome | Reported result on the new build |
| --- | --- | --- | --- |
| KAN-001 | Open the welcome screen in JetBrains, where the previous player was blank. | During playback, the viewer sees the Kanban demo advance through visibly different frames. | Pass. The demo plays. |
| KAN-002 | Open the welcome screen in VS Code, where the previous demo played. | During playback, the viewer sees the Kanban demo advance through visibly different frames. | Fail. The player shows a still frame. |

## Open boundaries

- How playback starts in either supported host is undecided. Both scenarios assess visible motion once playback is initiated.
- What the welcome screen shows on an unsupported host is undecided.
