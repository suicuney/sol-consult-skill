---
name: sol-high-plan-review
description: Use ChatGPT Web's GPT-5.6 Sol with High reasoning as an independent reviewer of a Codex-authored executable plan before implementation. Codex remains plan owner and final decision-maker. Use Chrome DevTools MCP as the only browser transport. Review may iterate up to 3 rounds, stopping early on PASS or escalating real product/architecture decisions to the user.
version: 2.0.0-alpha.2
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
→ 中文简版计划预览
→ 用户确认发送一次
→ Sol High Review
→ Codex Adopt / Reject / Modify
→ 必要时自动继续下一轮
→ 中文最终计划摘要
→ PLAN FROZEN
```

Maximum review rounds: `3`. Three is a limit, not a target.

## Default Policy

When this Skill is used inside AGY Supervised Development, plan review is enabled by default. If the user explicitly says to skip Sol review / skip plan review / execute directly, do not invoke this Skill.

## Review Preconditions

Codex must first form its own executable plan. The packet should contain only the evidence needed to review that plan.

Use `references/context-packet-template.md`.

Before browser submission:

```bash
python3 scripts/check_packet_safety.py packet.md
```

Use `scripts/build_attachment_bundle.py` only when many text files need one compact review artifact.

## User-visible Plan

Before the **first** browser Send, show the user a short Chinese summary of the plan being reviewed.

Keep it concise and easy to scan, normally:

```text
【准备发送给 Sol High 的计划】

目标
- <本次任务要完成什么>

计划
1. <关键动作>
2. <关键动作>
3. <关键动作>

重点风险
- <真正需要注意的风险；没有则省略>
```

This is a user-facing summary, not a dump of the full review packet. Do not replace it with packet size, character count, attachment size, or filenames alone.

After showing this summary, ask for **one** confirmation to send the first review request.

Once the user confirms the first Send:

- `REVISE` rounds continue automatically in the same verified conversation after Codex updates the plan;
- do not ask the user to confirm every review round;
- only interrupt the user for `USER_DECISION_REQUIRED`, a real one-way decision, authentication handoff, ambiguous Send state, or another genuine blocker.

## Browser Path

Use **Chrome DevTools MCP only**.

Read `references/mcp-workflow.md` before browser work.

Required ChatGPT state:

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

One or more concrete blocking findings can be fixed without a new user decision. Codex classifies meaningful recommendations as `Adopt`, `Reject`, or `Modify`, rewrites the plan, and may continue automatically to the next review round.

### USER_DECISION_REQUIRED

A real product, architecture, compatibility, destructive, security, cost, or other one-way trade-off requires the user. Stop the model-to-model loop and ask the user. Do not let either model invent the decision.

## Convergence Rule

Continue only when a **blocking** issue remains and another review round can materially improve the plan.

Exit when any of these is true:

```text
PASS
only non-blocking suggestions remain
USER_DECISION_REQUIRED
review_round == 3
```

If round 3 still contains unresolved blocking disagreement, return a compact user decision brief instead of starting round 4.

## Final Plan Output

When the review converges without a user decision blocker, return a concise Chinese final-plan summary to the calling workflow.

Suggested shape:

```text
【最终执行计划】

Sol High 评审：PASS | 已收敛
评审轮次：<n>

最终计划
1. <最终动作>
2. <最终动作>
3. <最终动作>

评审后的主要调整
- <有则列出；没有可写“无关键调整”>
```

This final summary is for visibility only. Do **not** request another confirmation before `PLAN FROZEN` unless a real user decision is still unresolved.

## Frozen Boundary

Once Codex records `PLAN FROZEN`, this Skill exits the task.

Do not call Sol High again during AGY implementation, Three-Axis Review, Rework, Independent Verification, browser runtime verification, Closeout, or Acceptance.

After plan freeze, repository and runtime evidence are more important than another model opinion.

## Completion Output

Return to the calling workflow:

```text
review_status = pass | revised | user_decision_required | unavailable
review_rounds = 0..3
blocking_findings = [...]
non_blocking_notes = [...]
adoption_decisions = Adopt / Reject / Modify
final_plan_summary_zh = <concise Chinese final plan>
final_plan_status = frozen | needs_user | not_reviewed
```

The authoritative executable plan remains the Codex-authored plan, not the raw Sol High response.
