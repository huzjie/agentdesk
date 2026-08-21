# 安全（零信任）

对齐 Google 零信任 AI 智能体架构：安全边界从「提示词」上移到「系统架构」。

## 分层防线

1. **策略引擎（Policy）**：拒绝式默认，规则 `allow`/`deny`，支持 `*` 通配。
2. **权限门禁（PermissionGate）**：动作执行前强制授权。
3. **沙箱（Sandbox）**：`subprocess` / `docker` / `none` 三种隔离模式。
4. **审计（Audit）**：追加式 JSONL 日志，记录谁在何时做了什么。

## 示例

```python
from agentdesk.security import PolicyEngine, PermissionGate
from agentdesk.security.policy import DEFAULT_RULES

gate = PermissionGate(PolicyEngine(DEFAULT_RULES))
gate.authorize("screenshot")        # ok
gate.authorize("shell")             # ForbiddenError
```
