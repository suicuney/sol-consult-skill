# Sol High Plan Review — Chrome DevTools MCP Workflow

Use Chrome DevTools MCP as the single browser execution path for plan review.

## Purpose

This workflow sends a Codex-authored executable plan to ChatGPT Web, verifies **GPT-5.6 Sol + High**, retrieves the review, and returns it to Codex as advisory evidence.

Sol High is a **Plan Reviewer**, not the plan owner, writer, verifier, or acceptance authority.

## Preconditions

- Chrome DevTools MCP is available to Codex.
- A dedicated test/browser profile is preferred.
- ChatGPT Web is signed in.
- The account exposes GPT-5.6 Sol with the `High` reasoning option.

If these are not true, do not silently use Pro, Medium, Extra High, OpenCLI, or another browser stack.

## Model Truth Gate

Before sending, verify both:

```text
Model family = GPT-5.6 Sol
Reasoning     = High
```

Reject:

```text
Pro           # GPT-5.6 Sol Pro, not this workflow
Extra High
Medium
Instant
ambiguous High text outside the active model/reasoning control
```

Prefer fresh browser snapshots and semantic/accessible state over brittle hard-coded selectors. After changing model or reasoning level, verify the selected state again.

## Review Dispatch

1. Codex creates the executable plan and its local judgment first.
2. Build the review packet from `context-packet-template.md`.
3. Run `scripts/check_packet_safety.py` before browser submission.
4. Upload only the minimum required artifacts. Use `scripts/build_attachment_bundle.py` when many text files need one reviewable bundle.
5. Insert the complete packet into the ChatGPT composer.
6. Verify the packet prefix, unique sentinel, model family, reasoning level, and required attachment names before Send.
7. Send once.

Do not inspect or export cookies, passwords, session databases, API keys, tokens, private keys, or unrelated authenticated browser data.

## Duplicate-Send Safety

Track only three dispatch states:

```text
NOT_SENT
SENT
UNKNOWN
```

- `NOT_SENT`: Send definitely was not clicked; rebuilding the draft is safe.
- `SENT`: submission evidence exists; recover the same conversation.
- `UNKNOWN`: connection/reset happened around Send; recover the existing conversation and never submit a duplicate.

If the original conversation cannot be identified safely, mark the review incomplete rather than sending again.

## Completion Gate

A review is complete only when:

```text
GPT-5.6 Sol confirmed
High confirmed
assistant generation finished
latest assistant turn extracted
expected sentinel is present in that assistant turn
```

Return the complete structured review to Codex. Codex then decides `Adopt / Reject / Modify` for every blocking recommendation that affects the next plan revision.

## Failure Rule

If Chrome DevTools MCP, ChatGPT login, GPT-5.6 Sol, or High is unavailable, report the missing capability truthfully.

Do not silently fall back to another model or transport. The calling workflow decides whether to fix the capability, disable plan review, or ask the user.
