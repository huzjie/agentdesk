# FAQ

**Q：核心真的零依赖吗？**
A：`agentdesk/` 业务内核仅用 Python 标准库。FastAPI 只在 `api/` 层按需引入。

**Q：没有 API Key 能跑吗？**
A：能。默认 `mock` provider + `mock` computer，全链路离线可跑。

**Q：如何接真实模型？**
A：在 `config.json` 的 `providers` 填 base_url / api_key / model，或设环境变量。

**Q：Computer Use 能真实操作桌面吗？**
A：把 `computer.mode` 设为 `pyautogui` 并安装 pyautogui 即可。
