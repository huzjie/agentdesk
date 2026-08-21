# Computer Use（计算机操作）

对标 Anthropic Computer Use 与 Qwen-UI-Agent：让数字员工像人一样操作屏幕、键盘、鼠标与浏览器。

## 动作模型

| 动作 | 参数 | 说明 |
|------|------|------|
| `screenshot` | `save` | 捕获屏幕 |
| `click` | `x`, `y`, `button` | 鼠标点击 |
| `double_click` | `x`, `y` | 双击 |
| `move` | `x`, `y` | 移动鼠标 |
| `type_text` | `text` | 键入文本 |
| `press` | `keys` | 组合键 |
| `scroll` | `clicks` | 滚动 |
| `browser_navigate` | `url` | 打开页面 |
| `browser_click` | `url`, `link_text` | 点击链接 |

## 三种运行模式

- `mock`（默认）：合成虚拟桌面，完全离线可测。
- `pyautogui`：真实 GUI 自动化（需 `pip install pyautogui`）。
- `browser`：浏览器操作（`urllib` 静态提取，或接入 Selenium/Playwright）。

## 步骤护栏与审批

`max_steps` 限制单个脚本的最大步数；`require_approval` 可对危险动作（如 `shell`）强制显式审批，未审批直接拒绝。

## 示例

```python
from agentdesk.computer import ComputerExecutor
from agentdesk.schema import Action

ex = ComputerExecutor(mode="mock")
ex.run_script([
    Action(type="screenshot"),
    Action(type="click", params={"x": 100, "y": 50}),
    Action(type="type_text", params={"text": "hello"}),
])
```
