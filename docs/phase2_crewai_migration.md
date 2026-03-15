# Phase 2：迁移到 CrewAI 的路线

当你已经跑通本地 MVP 后，再开始迁移到 CrewAI。

## 为什么这时再迁

因为这时你已经有：
- 固定的角色 prompt
- 固定的输出文件格式
- 固定的流程顺序
- 明确的输入输出边界

这时迁移成本最低。

## 推荐迁移顺序

1. 先迁 Product Manager + Architect + Engineer
2. 再加 Project Manager
3. 最后加 Admin Assistant 和 UI Designer

## 你要迁移的东西

### 1. 把 prompts.py 拆到 YAML

- Product Manager → `agents.yaml`
- Architect → `agents.yaml`
- Engineer → `agents.yaml`

### 2. 把 router.py 拆到 tasks.yaml

- `build_prd`
- `build_architecture`
- `build_dev_plan`

### 3. 把输出目录保持不变

保持这些输出路径不变：

```text
projects/<project>/prd/prd_full.md
projects/<project>/prd/prd_structured.json
projects/<project>/architecture/technical_design.md
projects/<project>/reports/dev_execution_guide.md
```

## 建议

迁移时，不要同时改：
- prompt 内容
- 目录结构
- 输出文件名
- agent 数量

一次只改一个变量。
