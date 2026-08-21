# CLI

```bash
agentdesk version                              # 版本
agentdesk doctor                               # 自检
agentdesk skill load                           # 加载内置技能
agentdesk skill list                           # 技能列表
agentdesk employee list                        # 员工列表
agentdesk employee create --name Alice         # 创建员工
agentdesk employee onboard --id <id>           # 入职
agentdesk employee transition --id <id> --action pause
agentdesk computer screen                      # 截屏
agentdesk computer run --actions '[{"type":"click","params":{"x":1,"y":1}}]'
agentdesk files list                           # 工作区文件
agentdesk academy courses                      # 课程
agentdesk academy assess --employee-id <id> --course-id crs_onboarding
agentdesk task "write a report"                # 跑任务
agentdesk serve --port 8500                    # 启动控制面
```
