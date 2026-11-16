# Kanban welcome demo

Hold the tested build. The owner requires moving video on the Kanban welcome screen in both JetBrains and VS Code. The owner reports that JetBrains now plays the demo, but VS Code shows a still frame.

## Watch the welcome demo

For each scenario, open the Kanban welcome screen in the named host and observe the demo when playback is expected. Visible motion in the demo is the acceptance criterion. A blank player or a single static video frame fails. The owner did not specify a playback trigger or require observation through the final step.

| Scenario and revision | Expected behavior | Reason for checking | Expectation review | New-build observation |
| --- | --- | --- | --- | --- |
| DEMO-JB r1 · JetBrains | The welcome demo plays moving video. | The previous player appeared blank. | Owner-approved | Pass, owner reports the demo plays. |
| DEMO-VSC r1 · VS Code | The welcome demo plays moving video. | The previous build played the demo in VS Code. | Owner-approved | Fail, owner reports a still frame. |
| DEMO-OTHER r1 · Unsupported host | Open decision. No expected presentation has been selected. | The owner has deferred the fallback decision. | Pending | No observation reported. |

## Decision and evidence

The owner's new-build report establishes the motion requirement for both named hosts and supplies the observations above. Unsupported-host presentation remains outside this release decision. Two expectations are approved and one is pending. The build has one reported pass and one reported failure. Verify both approved scenarios on the next release candidate before shipping.

This directory contains no build, video, or executable checks. There are no runner case IDs or independent playback results.
