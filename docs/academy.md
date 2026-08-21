# Academy（教学与认证）

对标 Anthropic Claude Academy，提供数字员工的培训与评估闭环。

## 4D AI Fluency Framework

| 维度 | 含义 |
|------|------|
| Discover | 理解上下文、定位信息与技能 |
| Develop | 构建并产出交付物 |
| Deploy | 安全可靠地操作工具与软件 |
| Drive | 自我改进与结果交付 |

## 评估

```python
result = assessor.assess("emp_1", "crs_onboarding", scores={
    "discover": 0.9, "develop": 0.8, "deploy": 0.85, "drive": 0.75,
})
# result.passed / result.scores
```

## 认证

全部评估通过即颁发认证，落盘到 `certifications/<employee_id>.json`。
