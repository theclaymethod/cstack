# Bootstrap: define password-reset behavior

This is a proposed feature. The existing synthetic spec covers VPN support, with password guidance as nearby preserved behavior; it does not approve password-reset actions.

Handoff:

> Use Bootstrap to help me define password-reset support. Interview me about the intended behavior, generate a small diverse scenario batch with subagents where available, and show guessed expectations for approval, correction, or deferral. Keep questions about product intent. Use this project's native case format and runner, preserve existing VPN behavior, and keep unreviewed cases out of the authoring handoff. Save work under eval-runs/password-bootstrap. Do not assume a password mention authorizes a ticket or an account action.

Answer the interview, then approve a few exact cards, correct one, and defer another. Leave at least one boundary unresolved to observe the partial-completion path. Real decisions you make here are separate from the prewritten synthetic exercise spec.

Completion: a versioned approved handoff, preserved correction history, and an explicit pending queue. The skill can prepare contract-based cases before password actions exist; execution limitations remain visible. Author approved cases in a separate `evals/generated/` file rather than rewriting a running campaign's core suite.
