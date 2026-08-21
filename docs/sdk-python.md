# Python SDK

```python
from agentdesk.sdk import AgentDeskClient

c = AgentDeskClient("http://127.0.0.1:8500")
c.healthz()
emp = c.create_employee("Alice", role="analyst")
c.transition_employee(emp["id"], "onboard")
c.run_task("write a report", employee_id=emp["id"])
```
