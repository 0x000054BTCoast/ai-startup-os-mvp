# AI Startup OS MVP 开发指南

这是一份给 **0 coding 经验产品经理** 直接使用的启动版开发指南。

这份 starter 的目标不是一上来搭完整的 6 个平级 Agent 公司，而是先跑通你文档里最关键的 **Week 1 最小生产链**：

```text
CEO 指令 → Product Manager Agent → Architect Agent → Fullstack Engineer Agent
```

等你先跑通这条链，再加：
- Telegram 通知
- Project Manager Agent
- Admin Assistant Agent
- n8n 自动化
- UI Designer Agent

---

## 1. 你现在要做什么

你只需要完成 5 件事：

1. 安装 Python 和 Git
2. 配置 DeepSeek API Key
3. 运行本项目
4. 输入一句产品目标
5. 查看自动生成的 PRD / 技术方案 / 开发指南

你不用先学会前端、后端、Docker、n8n、LangGraph。

---

## 2. 这份 MVP 为什么这样设计

我刻意把你的原始方案做了一个“能跑优先”的收敛：

- **保留**：CEO Router 思路、岗位分工、结构化输出、Company Memory Repo
- **暂不强上**：n8n 自托管、完整 CrewAI Flow、复杂状态机、数据库
- **原因**：你是 0 coding 经验，先把最小链路跑通最重要

这并不是推翻你原来的方案，而是把它拆成了更容易成功的第一步。

---

## 3. 当前这份 starter 能做什么

运行后，它会自动生成：

```text
projects/<project-name>/
  prd/
    prd_full.md
    prd_structured.json
  architecture/
    technical_design.md
  reports/
    dev_execution_guide.md
```

也就是说，你输入一句 CEO 指令后，系统会：

1. 让 Product Manager Agent 写 PRD
2. 让 Product Manager Agent 再输出结构化 JSON
3. 让 Architect Agent 基于 PRD 出技术方案
4. 让 Engineer Agent 出“你下一步怎么开发”的执行指南

---

## 4. 目录结构说明

```text
ai-startup-os-mvp/
  .env.example
  requirements.txt
  README_开发指南.md
  scripts/
    setup_mac.sh
  src/
    main.py
    bot_telegram.py
    agents/
      prompts.py
      product_manager.py
      architect.py
      engineer.py
    core/
      llm.py
      router.py
    utils/
      files.py
  .company-os/
    00_ceo_briefs/
    01_prd/
    02_architecture/
    03_tasks/
    04_ui_specs/
    05_daily_reports/
    06_decisions/
    07_prompts/
    08_templates/
  projects/
```

---

## 5. 环境要求

建议环境：

- macOS
- Python 3.11
- Git
- 一个 DeepSeek API Key

这份 starter 当前不要求 Docker、不要求数据库、不要求 Node.js。

---

## 6. 安装步骤（Mac）

### 第 1 步：安装 Homebrew

先在终端执行：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装完成后，执行：

```bash
brew --version
```

能看到版本号就可以。

### 第 2 步：安装 Python 3.11 和 Git

```bash
brew install python@3.11 git
```

检查：

```bash
python3.11 --version
git --version
```

### 第 3 步：进入项目目录

```bash
cd /你的项目目录/ai-startup-os-mvp
```

### 第 4 步：一键安装依赖

```bash
bash scripts/setup_mac.sh
```

它会自动做这些事：
- 创建 `.venv`
- 安装 Python 依赖
- 复制 `.env.example` 为 `.env`

### 第 5 步：填写 API Key

打开 `.env`，把：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

改成你自己的 key。

---

## 7. 如何拿到 DeepSeek API Key

去 DeepSeek 平台申请 API key，然后填到 `.env` 里。

`.env` 最少要这样：

```env
DEEPSEEK_API_KEY=你的key
DEEPSEEK_BASE_URL=https://api.deepseek.com
MODEL_PRODUCT=deepseek-chat
MODEL_ARCHITECT=deepseek-reasoner
MODEL_ENGINEER=deepseek-reasoner
DEFAULT_PROJECT_NAME=demo-project
TIMEZONE=Asia/Tokyo
```

---

## 8. 第一次运行

先激活虚拟环境：

```bash
source .venv/bin/activate
```

然后执行：

```bash
python src/main.py --goal "为 PRD2Prototype 写一份可开发 PRD、技术方案和开发执行指南"
```

运行成功后，终端会打印类似：

```text
=== Done ===
Project: projects/demo-project
PRD: projects/demo-project/prd/prd_full.md
PRD JSON: projects/demo-project/prd/prd_structured.json
Architecture: projects/demo-project/architecture/technical_design.md
Dev Guide: projects/demo-project/reports/dev_execution_guide.md
```

然后你直接去这些文件里看结果。

---

## 9. 你每次怎么使用它

以后每次只做这 3 步：

### 场景 A：你想定义一个新项目

```bash
python src/main.py --project prd2prototype --goal "做一个本地工具：上传 PRD markdown，输出 structured json，再生成 html 和 svg 原型图"
```

### 场景 B：你想让它帮你写交易页需求

```bash
python src/main.py --project trading-page --goal "为交易所现货交易页输出一份 AI 可消费的 PRD 和前端开发执行指南"
```

### 场景 C：你想先写登录注册系统

```bash
python src/main.py --project auth-system --goal "为登录注册页面生成 PRD、结构化需求 JSON 和开发任务执行指南"
```

---

## 10. 当前 3 个 Agent 的职责

### Product Manager Agent

负责输出：
- `prd_full.md`
- `prd_structured.json`

### Architect Agent

负责输出：
- `technical_design.md`

### Fullstack Engineer Agent

负责输出：
- `dev_execution_guide.md`

你暂时先不要上 6 个 agent 一起跑。

---

## 11. 为什么现在不先强上 CrewAI / n8n / Docker

原因非常现实：

### CrewAI
适合多角色协作、YAML 脚手架、flow、memory、knowledge，但第一天就上完整 crew 编排，会增加你的心智负担。

### n8n
适合自动化，但自托管对运维要求更高。

### Docker
适合后续把环境标准化，但你刚开始最重要的是先看到系统真的在输出文件。

所以这版 starter 先用：
- Python
- DeepSeek API
- 本地文件夹当知识库
- 可选 Telegram

这才是最适合你起步的版本。

---

## 12. Telegram 可选接入

如果你想把它变成“发 Telegram 消息触发”的系统，可以用 `src/bot_telegram.py`。

### 第 1 步：创建 Telegram Bot

在 Telegram 里找到 `@BotFather`，创建一个新 bot，拿到 token。

### 第 2 步：拿到你的 chat id

最简单的办法：
1. 先给 bot 发一条消息
2. 浏览器打开：

```text
https://api.telegram.org/bot<你的token>/getUpdates
```

3. 返回 JSON 里找到 chat.id

### 第 3 步：配置 `.env`

```env
TELEGRAM_BOT_TOKEN=你的bot token
TELEGRAM_CHAT_ID=你的chat id
```

### 第 4 步：启动 bot

```bash
source .venv/bin/activate
python src/bot_telegram.py
```

然后你给 bot 发一句：

```text
为 PRD2Prototype 写 PRD 和技术方案
```

它就会在本地生成文件，并回你一条结果路径。

---

## 13. 常见报错与解决

### 1）`Missing DEEPSEEK_API_KEY in .env`

说明 `.env` 没填 key。

处理：
- 打开 `.env`
- 检查 `DEEPSEEK_API_KEY=...`
- 保存后重新运行

### 2）`ModuleNotFoundError: No module named 'openai'`

说明依赖没装好。

处理：

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### 3）`401 Unauthorized`

说明 DeepSeek key 错了或者没权限。

处理：
- 换正确 key
- 检查 API 平台余额和权限

### 4）`json decode error`

说明模型这次输出的 JSON 不规范。

处理：
- 再跑一次
- 把 goal 写得更明确
- 避免一条命令里塞太多目标

### 5）Telegram 没响应

处理顺序：
- 检查 `TELEGRAM_BOT_TOKEN`
- 检查 `TELEGRAM_CHAT_ID`
- 先给 bot 发过消息没有
- 再手动访问 `getUpdates`

---

## 14. 你下一步该怎么迭代

### 第 1 周
先把这个 starter 跑通。

目标：
- 你能稳定生成 PRD
- 你能稳定生成技术方案
- 你能稳定生成开发执行指南

### 第 2 周
加两个角色：
- Project Manager Agent
- Admin Assistant Agent

增加输出：
- `task_breakdown.json`
- `daily_progress.md`
- `blockers.md`

### 第 3 周
加 UI Designer Agent。

增加输出：
- `ui_design_spec.md`
- `design_tokens.json`
- `component_states.md`

### 第 4 周
再决定要不要引入：
- CrewAI
- n8n
- Docker
- LangGraph

---

## 15. 你怎么判断这套东西已经“跑通”

只看 4 个标准：

1. 你一句 CEO 指令能生成文件
2. 生成的 PRD 不是空话，而是结构化的
3. 技术方案不是概念图，而是有模块边界
4. 开发指南能告诉你“接下来改哪些文件、跑哪些命令”

只要这 4 点满足，你就已经不是在“聊概念”，而是在真的搭自己的 AI Startup OS 了。

---

## 16. 未来迁移到 CrewAI 的时机

当你出现这几个信号时，再迁：

- 你已经稳定有 4 个以上固定角色
- 你想用 YAML 管理 agent 配置
- 你想让流程更标准化
- 你想增加 memory / knowledge / flow / observability

这时再把当前 `src/agents/` 的 prompt 和职责迁移到 CrewAI。

---

## 17. 最后给你的实际建议

你现在不要想着：
- 一次做完公司级系统
- 一次搞定 6 个 agent
- 一次接上 n8n、Telegram、Notion、GitHub、Figma

你现在只要做这一件事：

> **把“输入一句 CEO 指令 → 输出 PRD / 技术方案 / 开发指南”先跑通。**

这是你整套 AI 公司最重要的第一块地基。

