# sol-consult-skill

一个用于 **GPT-5.6 Sol High 可执行方案评审** 的私人 Skill。

当前版本：**2.0.0-alpha.1**。

## 定位

这个 Skill 只做一件事：

> 在实现开始前，让 ChatGPT Web 的 GPT-5.6 Sol + High 对 Codex 已经写好的可执行方案做一次独立评审。

角色固定：

```text
Codex = Plan Owner
Sol High = Plan Reviewer
Chrome DevTools MCP = Browser Transport
User = Product / One-way Decision Authority
```

Sol High 不接管方案，不写代码，不参与实现后的 Review / Verification / Closeout。

## 默认流程

```text
Codex Plan v0
→ Sol High Review
→ Codex Adopt / Reject / Modify
→ Plan v1
→ 最多 3 轮
→ PLAN FROZEN
→ Sol High 退出
```

- 默认启用方案评审；
- 用户明确要求跳过时直接跳过；
- `PASS` 可提前结束，不要求跑满 3 轮；
- 出现真实产品/架构取舍时交还用户；
- 第 3 轮仍有 blocking disagreement 时停止模型循环，不进入第 4 轮。

## 浏览器执行

唯一支持路径：

```text
Codex
→ Chrome DevTools MCP
→ ChatGPT Web
→ GPT-5.6 Sol
→ High
```

不再维护：

```text
Codex Chrome Plugin
OpenCLI fallback
自定义 OpenCLI browser runner
GPT-5.6 Sol Pro 路径
```

如果 MCP、登录状态、GPT-5.6 Sol 或 High 不可用，真实报告缺失能力，不静默切换其它模型或浏览器控制栈。

## 目录

```text
sol-consult-skill/
├── SKILL.md
├── README.md
├── UPSTREAM.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── evals/
│   └── evals.json
├── references/
│   ├── mcp-workflow.md
│   └── context-packet-template.md
├── scripts/
│   ├── build_attachment_bundle.py
│   └── check_packet_safety.py
└── tests/
    └── test_skill_contract.py
```

## 核心边界

1. Codex 必须先形成自己的可执行方案。
2. Sol High 只返回 `PASS | REVISE | USER_DECISION_REQUIRED`。
3. Codex 对重要建议执行 `Adopt / Reject / Modify`。
4. 最多 3 轮评审；Non-blocking / Backlog 不维持循环。
5. `PLAN FROZEN` 后 Sol High 不再参与本次任务。
6. AGY、Git、测试和运行时证据负责实现后的真实交付证明。

## 与 AGY Supervised Development 的关系

推荐把这个 Skill 作为 AGY 流程的 **Plan Review Gate**：

```text
Requirement
→ Codex Executable Plan
→ Sol High Plan Review
→ PLAN FROZEN
→ AGY Build
→ Codex Review
→ Codex Verify / Chrome DevTools MCP
→ Closeout
→ Accepted
```

这是一条串行流程，不引入新的 orchestrator、review manager 或 capability router。

## Upstream

最初来源与导入基线见 [`UPSTREAM.md`](./UPSTREAM.md)。Git history 保留了此前 GPT-5.6 Sol Pro / Chrome Plugin / OpenCLI 版本的完整演进记录。
