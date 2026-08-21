# AgentDesk — 企业级 AI 数字员工运营平台

> **Enterprise Digital Workforce Operations Platform**
> 把大模型变成「可管理、可教学、可操作电脑、可交付文件」的数字员工。

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-3776AB)
![License](https://img.shields.io/badge/license-Apache--2.0-green)
![Zero-deps](https://img.shields.io/badge/core-zero--dependency-orange)

---

## 这是什么？

2026 年 8 月，AI 的叙事发生了一次根本转向：**从「会聊天的助手」变成「会干活的数字员工」**。

- **Anthropic 上线 Computer Use / Skills API / Files API** —— Claude 智能体现在能直接操作软件、调用团队预设技能、生成并返回成品文件；
- **Claude Academy + 4D AI Fluency Framework** —— 企业开始给 AI 员工做「入职培训」；
- **阿里 Qwen-UI-Agent** —— 让模型真正「看懂并操作」每一寸屏幕；
- **Mistral Agentic Search** —— 五步循环自主查资料；
- **Google 零信任 AI 智能体架构** —— 把安全边界从「提示词」上移到「系统架构」。

**AgentDesk 是这一趋势的自托管落地实现**：一套完整平台，让企业像管理人类员工一样管理 AI 数字员工 —— 入职、赋技能、操作电脑、产出文件、培训认证、零信任审计，全流程闭环。

## 核心能力一览

| 模块 | 对标能力 | 说明 |
|------|----------|------|
| 🧑💼 **Workforce** | 数字员工目录 | 员工注册、生命周期状态机、入职编排 |
| 🧩 **Skills** | Skills API | 可复用技能库，SemVer 版本化、倒排搜索、内置技能目录 |
| 🖥️ **Computer Use** | Computer Use | 屏幕/鼠标键盘/浏览器操作抽象 + 动作执行器 + 步骤护栏 |
| 📁 **Files** | Files API | 沙箱工作区、产物追踪（sha256）、交付打包 |
| 🎓 **Academy** | Claude Academy | 课程目录 + 4D AI Fluency 评估 + 认证颁发 |
| 🔐 **Security** | 零信任 | 策略引擎、权限门禁、沙箱、追加审计日志 |
| 🤖 **Agents** | 执行循环 | ReAct 风格工具调用循环，mock 模式完全离线 |
| 🔌 **Providers** | 多模型 | OpenAI/Anthropic/DeepSeek/Qwen/Kimi/GLM/Gemini/Ollama/Mock |
| 📊 **Observability** | 监控 | Prometheus 指标 + W3C traceparent 追踪 |
| 🗄️ **Storage** | 持久化 | SQLite（纯标准库） |

**核心内核零第三方运行时依赖**（纯 Python 标准库），`mock` 模式开箱即用、完全离线可跑。

## 项目结构

```
agentdesk/
├── agentdesk/              # 核心 Python 包（纯标准库）
│   ├── workforce/          # 数字员工：目录、状态机、入职
│   ├── skills/             # 技能体系：注册、版本、目录
│   ├── computer/           # Computer Use：屏幕、输入、浏览器、执行器
│   ├── files/              # Files API：工作区、产物、交付
│   ├── academy/            # 教学：课程、4D 框架、评估、认证
│   ├── security/           # 零信任：策略、权限、沙箱、审计
│   ├── observability/      # 指标 + 追踪
│   ├── storage/            # SQLite 持久化
│   ├── agents/             # 工具注册 + 执行循环
│   ├── providers/          # 9 家 LLM Provider 适配器
│   ├── api/                # FastAPI 控制面
│   ├── cli/                # 命令行
│   └── sdk/                # Python SDK
├── ts-sdk/                 # TypeScript SDK
├── console/                # React 18 + Vite 控制台
├── tests/                  # 30+ 单元测试（stdlib unittest）
├── docs/                   # 18+ 篇文档
├── examples/               # 可运行示例
├── k8s/ helm/ monitoring/  # Kubernetes + Helm + Prometheus/Grafana
├── Dockerfile / docker-compose.yml
└── .github/workflows/      # CI + CodeQL
```

## 快速开始（30 秒，零依赖）

```bash
git clone https://github.com/huzjie/agentdesk.git
cd agentdesk
pip install -e .            # 核心零依赖，直接可用

# 1) 自检
agentdesk doctor

# 2) 加载内置技能库
agentdesk skill load

# 3) 创建并入职一个数字员工
agentdesk employee create --name "Alice" --role analyst
agentdesk employee onboard --id <employee_id>

# 4) 跑一个任务（mock 模式离线可跑）
agentdesk task "write a report file"

# 5) 启动控制面（可选，需要 fastapi/uvicorn）
pip install -e ".[api]"
agentdesk serve
```

然后打开浏览器访问 `http://127.0.0.1:8500/docs`（OpenAPI 文档）或启动 React 控制台：

```bash
cd console && npm install && npm run dev   # http://localhost:5173
```

## 配置真实模型（填写即可运行）

核心内核零依赖，但接入真实 LLM 只需在 `config.json` 或环境变量里填上凭证：

```json
{
  "providers": {
    "default": "deepseek",
    "deepseek": {
      "base_url": "https://api.deepseek.com/v1",
      "api_key": "sk-你的密钥",
      "model": "deepseek-chat"
    }
  }
}
```

或用环境变量（`__` 表示层级）：

```bash
export AGENTDESK_PROVIDERS__DEFAULT=deepseek
export AGENTDESK_PROVIDERS__DEEPSEEK__API_KEY=sk-你的密钥
export AGENTDESK_PROVIDERS__DEEPSEEK__MODEL=deepseek-chat
```

支持的 Provider：`openai` / `anthropic` / `deepseek` / `qwen` / `kimi` / `glm` / `gemini` / `ollama` / `mock`。

## 为什么值得用

- **零依赖内核**：核心逻辑纯 Python 标准库，任何环境 `pip install -e .` 即可跑，无编译、无 C 扩展。
- **离线可测**：`mock` provider + `mock` computer 让整个链路（入职→技能→任务→文件）离线端到端跑通。
- **安全优先**：拒绝式默认 + 策略引擎 + 沙箱 + 追加审计，对齐「零信任 AI 智能体」范式。
- **生产资产齐全**：Docker / docker-compose / K8s / Helm / Prometheus+Grafana / CI + CodeQL。
- **文档完善**：18+ 篇文档覆盖架构、安全、部署、SDK、API、FAQ。

## 文档导航

- [快速开始](docs/quickstart.md) · [架构](docs/architecture.md) · [核心概念](docs/concepts.md)
- [Computer Use](docs/computer-use.md) · [技能体系](docs/skills.md) · [Files API](docs/files-api.md) · [Academy](docs/academy.md)
- [安全](docs/security.md) · [配置](docs/config.md) · [CLI](docs/cli.md) · [API 参考](docs/api-reference.md)
- [部署](docs/deployment.md) · [Python SDK](docs/sdk-python.md) · [TS SDK](docs/sdk-typescript.md) · [测试](docs/testing.md)

## 许可证

[Apache-2.0](LICENSE)
