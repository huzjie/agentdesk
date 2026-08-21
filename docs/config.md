# 配置

配置优先级：**环境变量 > JSON 文件 > 内置默认值**。

## config.json

```json
{
  "agentdesk": { "workspace_root": "~/.agentdesk/workspace", "db_path": "~/.agentdesk/agentdesk.db" },
  "server": { "host": "127.0.0.1", "port": 8500 },
  "computer": { "mode": "mock", "max_steps": 20 },
  "security": { "sandbox": "subprocess", "deny_network": false, "require_approval": ["shell"] },
  "academy": { "pass_threshold": 0.7 },
  "providers": { "default": "mock", "deepseek": { "base_url": "https://api.deepseek.com/v1", "api_key": "sk-xxx", "model": "deepseek-chat" } }
}
```

## 环境变量

前缀 `AGENTDESK_`，`__` 表示层级：

```bash
export AGENTDESK_PROVIDERS__DEFAULT=qwen
export AGENTDESK_PROVIDERS__QWEN__API_KEY=sk-xxx
export AGENTDESK_COMPUTER__MODE=mock
```
