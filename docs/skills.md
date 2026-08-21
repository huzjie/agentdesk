# 技能体系（Skills API）

## 注册技能

```python
from agentdesk.skills import SkillRegistry, SkillDef

reg = SkillRegistry()
reg.register(SkillDef(
    name="text_summary",
    version="1.0.0",
    description="Summarize text",
    category="content",
    parameters=[{"name": "text", "type": "string", "required": True}],
    tags=["summarize", "nlp"],
))
```

## 版本与搜索

- SemVer 版本化：同名技能可并存多个版本，`get_by_name` 返回最新版。
- 关键词搜索：`list(query="summary")` 对名称/描述/标签做倒排匹配。

## 内置技能目录

`load_catalog(reg)` 一键注册 6 个内置技能。CLI：`agentdesk skill load`。
