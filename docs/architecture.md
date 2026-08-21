# 架构

AgentDesk 采用分层架构，内核与边界严格解耦：

```
┌─────────────────────────────────────────────────────┐
│  console (React)  │  CLI  │  Python SDK  │  TS SDK   │  ← 交互层
├─────────────────────────────────────────────────────┤
│              api (FastAPI 控制面, 可选)               │  ← HTTP 边界
├─────────────────────────────────────────────────────┤
│                    platform.py                       │  ← 组装层（单一装配点）
├──────────┬──────────┬──────────┬──────────┬─────────┤
│ workforce│ skills   │ computer │ files    │ academy │  ← 业务域
├──────────┼──────────┼──────────┼──────────┼─────────┤
│ security │ observability │ storage │ agents   │ providers│ ← 横切/基础设施
└─────────────────────────────────────────────────────┘
```

## 设计原则

1. **零依赖内核**：`agentdesk/` 下所有业务逻辑只用标准库；FastAPI 仅在 `api/` 层按需引入。
2. **拒绝式默认（Deny-by-default）**：策略引擎无匹配规则即拒绝，安全第一。
3. **单一装配点**：`Platform` 类集中装配所有子系统，CLI / API / SDK 共享同一实例。
4. **Mock 优先**：所有外部能力（模型、屏幕、浏览器、沙箱）都有 mock 实现，保证离线可测。

## 数据流（任务执行）

```
用户/API ──> run_task(task)
              │
              ▼
          AgentLoop ──> Provider.chat(messages)
              │  ▲
              │  └── <tool_call> 解析
              ▼
          ToolRegistry.invoke(name, **args)
              │
              ▼
          Workspace / 外部副作用  ← PermissionGate 授权 + AuditLog 记录
```

## 目录职责

| 目录 | 职责 |
|------|------|
| `workforce/` | 数字员工生命周期 |
| `skills/` | 技能注册、版本、搜索 |
| `computer/` | 屏幕/输入/浏览器/动作执行 |
| `files/` | 工作区、产物、交付 |
| `academy/` | 课程、4D 评估、认证 |
| `security/` | 策略、权限、沙箱、审计 |
| `storage/` | SQLite 持久化 |
| `agents/` | 工具注册 + 执行循环 |
| `providers/` | 多 Provider 适配器 |
