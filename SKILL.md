---
name: sol-high-plan-review
description: Use ChatGPT Web's GPT-5.6 Sol with High reasoning as an independent reviewer of a Codex-authored executable plan before implementation. Codex remains plan owner and final decision-maker. Use Chrome DevTools MCP as the only browser transport. Review may iterate up to 3 rounds, stopping early on PASS or escalating real product/architecture decisions to the user.
version: 2.0.0-alpha.1
---

# Sol High Plan Review

Use this Skill only to improve an executable development plan **before implementation starts**.

```text
Codex = Plan Owner
Sol High = Independent Plan Critic
Chrome DevTools MCP = Browser Transport
User = Product / One-way Decision Authority
```

Sol High never becomes the writer, runtime verifier, final reviewer, or acceptance authority.

## Core Flow

```text
Codex Plan v0
→ Sol High Review
→ Codex Adopt / Reject / Modify
→ Plan v1
→ optional next review
→ PLAN FROZEN
```

Maximum review rounds:

```text
3
```

Three is a limit, not a target. Stop as soon as the plan is good enough to execute.

## Default Policy

When this Skill is used inside AGY Supervised Development:

```text
Plan Review = enabled by default
```

If the user explicitly says to skip Sol review / skip plan review / execute directly, do not invoke this Skill.

## Review Preconditions

Codex must first form its own executable plan. The packet should contain only the evidence needed to review that plan.

Use `references/context-packet-template.md`.

Before browser submission:

```bash
python3 scripts/check_packet_safety.py packet.md
```

Use `scripts/build_attachment_bundle.py` only when many text files need one compact review artifact.

## Browser Path

Use **Chrome DevTools MCP only**.

Read `references/mcp-workflow.md` before browser work.

The required ChatGPT state is:

```text
Model family = GPT-5.6 Sol
Reasoning     = High
```

Do not silently substitute Pro, Extra High, Medium, another model, OpenCLI, or another browser controller.

## Review Contract

Sol High must return one verdict:

```text
PASS
REVISE
USER_DECISION_REQUIRED
```

### PASS

No blocking plan finding remains. Codex may freeze the plan.

### REVISE

One or more concrete blocking findings can be fixed without a new user decision.

Codex must classify meaningful Sol recommendations as:

```text
Adopt
Reject
Modify
```

Then Codex rewrites the plan and may start the next review round.

### USER_DECISION_REQUIRED

A real product, architecture, compatibility, destructive, security, cost, or other one-way trade-off requires the user.

Stop the model-to-model loop and ask the user. Do not let either model invent the decision.

## Convergence Rule

Continue only when a **blocking** issue remains and another review round can materially improve the plan.

Non-blocking suggestions and backlog ideas do not keep the loop open.

Exit when any of these is true:

```text
PASS
only non-blocking suggestions remain
USER_DECISION_REQUIRED
review_round == 3
```

If round 3 still contains unresolved blocking disagreement, return a compact user decision brief instead of starting round 4.

## Frozen Boundary

Once Codex records:

```text
PLAN FROZEN
```

this Skill exits the task.

Do not call Sol High again during:

```text
AGY implementation
Three-Axis Review
Rework
Independent Verification
Browser runtime verification
Closeout
Acceptance
```

After plan freeze, repository and runtime evidence are more important than another model opinion.

## Completion Output

Return to the calling workflow:

```text
review_status = pass | revised | user_decision_required | unavailable
review_rounds = 0..3
blocking_findings = [...] 
non_blocking_notes = [...]
adoption_decisions = Adopt / Reject / Modify
final_plan_status = frozen | needs_user | not_reviewed
```

The authoritative executable plan remains the Codex-authored plan, not the raw Sol High response.
