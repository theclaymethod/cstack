# Expert Mode: capture a correction

Invoke `$expert-mode`, then run:

```sh
python3 evaluate.py run --candidate support_agent.py --suite development --out eval-runs/expert-baseline
```

Inspect the how-to case's input, actual output, and resulting tickets. Tell the agent what you judge about that particular output. For example, if this matches your intent: “For this how-to question, creating a ticket is wrong; give guidance and leave tickets unchanged.” This suggested statement is not your approval until you actually supply it.

Add one uncertainty, such as whether urgent failures should escalate automatically, without resolving it. Ask the agent to retain that uncertainty separately.

Completion: a capture links your exact decision to the reviewed output/version and criterion. The unresolved boundary stays uncertain. The agent does not silently label unrelated cases or treat the suggested example sentence as something you said. Capturing feedback does not edit the product or rewrite its failed output.
