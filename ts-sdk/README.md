# @agentdesk/sdk

TypeScript SDK for the AgentDesk digital workforce platform.

```ts
import { AgentDeskClient } from "@agentdesk/sdk";

const client = new AgentDeskClient("http://127.0.0.1:8500");
const employees = await client.listEmployees();
const result = await client.runTask("Write a summary report");
```
