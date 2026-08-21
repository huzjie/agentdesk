# TypeScript SDK

```ts
import { AgentDeskClient } from "@agentdesk/sdk";

const c = new AgentDeskClient("http://127.0.0.1:8500");
const employees = await c.listEmployees();
const result = await c.runTask("write a report");
```
