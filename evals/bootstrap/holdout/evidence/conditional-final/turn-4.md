# Kanban welcome demo

After the video change, users must be able to watch moving video on the Kanban welcome screen in both VS Code and JetBrains. A still frame throughout playback fails this requirement.

| ID | Starting situation | Required outcome | Reported result on the new build |
| --- | --- | --- | --- |
| KAN-001 | Open the updated welcome demo in VS Code, where the previous video played. | The demo plays visibly moving video. | Fail. The demo shows a still frame. |
| KAN-002 | Open the updated welcome demo in JetBrains, where the previous player was blank. | The demo plays visibly moving video. | Pass. The demo plays. |

The current build fails the shipping requirement because KAN-001 fails.

Playback startup remains undecided. These scenarios assess visible motion during playback. Behavior on unsupported hosts is deferred, with no fallback specified for this release.
