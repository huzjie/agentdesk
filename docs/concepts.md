# 核心概念

## 数字员工（Employee）

数字员工是一个有身份、有状态、有技能、有培训记录的一等公民对象。

**生命周期状态机**：

```
provisioned ──onboard──▶ onboarding ──complete──▶ active
     ▲                      │                        │
     └──────fail────────────┘                 pause/offboard
                                                │        │
                                             paused ─────┘
                                                │ resume
                                                ▼
                                              active
```

## 技能（Skill）

技能是可复用的能力单元，带 SemVer 版本。平台内置 6 个开箱技能（文本摘要、邮件起草、网页查询、报告生成、屏幕捕获、表格填充）。

## 动作（Action）

Computer Use 的最小操作单元：`screenshot` / `click` / `type_text` / `press` / `scroll` / `browser_navigate` 等。

## 4D AI Fluency

评估数字员工的四个维度：**Discover**（理解上下文）、**Develop**（产出交付物）、**Deploy**（安全操作工具）、**Drive**（自我改进与结果交付）。

## 零信任

拒绝式默认 + 策略引擎 + 权限门禁 + 沙箱 + 追加审计，共同构成安全边界。
