# sol-consult-skill

一个用于维护和定制 **GPT 5.6 Sol Pro 第二意见 / 专家会诊工作流** 的私人 Skill 仓库。

当前 `main` 是从 `zjp1997720/zhijian-skills` 中独立抽出的 `gpt56-sol-pro-consult` 基线版本。第一步先保持原版行为稳定，后续再针对个人 Codex / AGY 开发流程逐步演进。

## 当前定位

这个 Skill 不让 Pro 直接接管任务，而是把它当作外部 Reviewer：

```text
Local Agent / Codex
    ↓
先形成自己的判断
    ↓
整理 Context Packet + 真实证据
    ↓
GPT 5.6 Sol Pro 第二意见
    ↓
Local Agent 验证
    ↓
Adopt / Reject / Modify
    ↓
最终结论
```

核心原则：**Pro 负责挑战，主 Agent 负责最终判断。**

## v1.0 baseline 保留内容

- Chrome-first 的 ChatGPT Web 会诊路径
- GPT 5.6 Sol + Pro 的模型真实性校验
- 真实附件上传要求
- Context Packet 模板
- 凭据 / Token / Cookie / API Key 等敏感信息扫描
- OpenCLI 文本模式 fallback
- Sentinel 完整响应校验
- 不确定发送状态下禁止重复提交
- Adopt / Reject / Modify 本地整合方式
- 原版 eval 与回归测试

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
│   ├── chrome-workflow.md
│   ├── context-packet-template.md
│   └── opencli-fallback.md
├── scripts/
│   ├── build_attachment_bundle.py
│   ├── check_packet_safety.py
│   ├── extract_chatgpt_reply.py
│   └── run_gpt56_sol_pro_consult.py
└── tests/
    ├── test_model_selection.py
    └── test_skill_contract.py
```

## 当前 Skill 身份

为了让第一版基线可直接与上游比较，内部 Skill 名暂时仍然是：

```text
gpt56-sol-pro-consult
```

仓库名是：

```text
sol-consult-skill
```

后续如果决定改 Skill ID、默认 Reviewer 或调用方式，应同步调整 `SKILL.md`、`agents/openai.yaml`、`evals/`、脚本和测试，不做只改名字的半迁移。

## 推荐的下一步定制方向

后续版本可以逐项演进，而不是一次性重写：

1. **Reviewer 可配置化**：把固定 GPT 5.6 Sol Pro 抽象为 Reviewer Profile，同时保留 Sol Pro 作为默认高质量 Reviewer。
2. **会诊场景分级**：增加 Plan Review、Architecture Review、Risk Review、Final Review 等模式。
3. **触发门槛**：普通小任务不调用 Pro，只在高成本决策、关键设计、复杂 Bug 或最终 Gate 时使用。
4. **AGY / Codex 集成**：让 AGY 决定是否进入会诊 Gate，Codex 保持主执行和最终裁决权。
5. **Context Packet 定制**：针对代码开发、Skill 设计、架构评审分别使用更聚焦的模板。
6. **结果结构化**：稳定输出分歧点、证据、风险、Adopt / Reject / Modify 和最终行动项。

## Upstream

来源与导入基线见 [`UPSTREAM.md`](./UPSTREAM.md)。

## License

基于 MIT 许可的上游实现继续演进；原版权与许可声明保留在 [`LICENSE`](./LICENSE)。
