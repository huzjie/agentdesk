# API 参考

启动后访问 `/docs` 查看交互式 OpenAPI。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/healthz` | 健康检查 |
| GET | `/version` | 版本 |
| GET | `/metrics` | Prometheus 指标 |
| GET/POST | `/employees` | 员工列表/创建 |
| POST | `/employees/{id}/transition` | 状态流转 |
| POST | `/employees/{id}/onboard` | 入职 |
| GET/POST | `/skills` | 技能列表/注册 |
| POST | `/skills/catalog/load` | 加载内置技能 |
| GET | `/computer/screen` | 截屏 |
| POST | `/computer/actions` | 执行动作 |
| GET/POST | `/files` | 文件列表/写入 |
| POST | `/files/artifacts` | 登记产物 |
| POST | `/files/bundle` | 打包交付 |
| GET | `/academy/courses` | 课程 |
| POST | `/academy/assess` | 评估 |
| POST | `/tasks` | 执行任务 |
| GET | `/audit` | 审计日志 |
