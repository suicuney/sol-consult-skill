# sol-consult-skill

一个用于 **GPT-5.6 Sol High 可执行方案评审** 的私人 Skill。

当前版本：**2.0.0-alpha.2**。

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
→ 中文简版计划给用户看
→ 用户确认发送一次
→ Sol High Review
→ Codex Adopt / Reject / Modify
→ 必要时自动继续下一轮
→ 中文最终计划给用户看
→ PLAN FROZEN
→ Sol High 退出
```

- 默认启用方案评审；
- 用户明确要求跳过时直接跳过；
- 第一轮发送前必须用中文简洁说明 `目标 / 计划 / 重点风险`；
- 第一轮发送只确认一次；
- 后续 `REVISE` 不反复要求确认，除非出现真实用户决策或 blocker；
- 收敛后展示中文最终计划，但不再次确认；
- `PASS` 可提前结束，不要求跑满 3 轮；
- 出现真实产品/架构取舍时交还用户；
- 第 3 轮仍有 blocking disagreement 时停止模型循环，不进入第 4 轮。

## 用户看到的计划

发送前：

```text
【准备发送给 Sol High 的计划】

目标
- ...

计划
1. ...
2. ...
3. ...

重点风险
- ...
```

评审结束后：

```text
【最终执行计划】

Sol High 评审：PASS / 已收敛
评审轮次：<n>

最终计划
1. ...
2. ...
3. ...

评审后的主要调整
- ...
```

这两个输出都强调“用户能看懂这次准备怎么做”，不会用 packet 字符数、文件大小或附件大小代替计划内容。

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
2. 第一轮 Send 前显示中文简版计划并只确认一次。
3. Sol High 只返回 `PASS | REVISE | USER_DECISION_REQUIRED`。
4. Codex 对重要建议执行 `Adopt / Reject / Modify`。
5. 后续可修复的 `REVISE` 自动继续，不重复询问 Send。
6. 最多 3 轮评审；Non-blocking / Backlog 不维持循环。
7. 收敛后显示中文最终计划，不再次确认。
8. `PLAN FROZEN` 后 Sol High 不再参与本次任务。
9. AGY、Git、测试和运行时证据负责实现后的真实交付证明。

## 与 AGY Supervised Development 的关系

推荐把这个 Skill 作为 AGY 流程的 **Plan Review Gate**：

```text
Requirement
→ Codex Executable Plan
→ 中文简版 Plan + 一次确认
→ Sol High Plan Review
→ 中文最终 Plan
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
