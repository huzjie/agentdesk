import { Employee, Skill, Course, TaskResult } from "./types";

export class AgentDeskClient {
  private baseUrl: string;
  private apiKey: string;

  constructor(baseUrl = "http://127.0.0.1:8500", apiKey = "") {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.apiKey = apiKey;
  }

  private async request<T>(method: string, path: string, body?: unknown): Promise<T> {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (this.apiKey) headers["Authorization"] = `Bearer ${this.apiKey}`;
    const res = await fetch(this.baseUrl + path, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`${method} ${path} -> ${res.status}`);
    return (await res.json()) as T;
  }

  healthz() { return this.request<{ status: string }>("GET", "/healthz"); }
  version() { return this.request<{ version: string }>("GET", "/version"); }

  listEmployees(status?: string) {
    return this.request<Employee[]>("GET", `/employees${status ? `?status=${status}` : ""}`);
  }
  createEmployee(name: string, role = "generalist") {
    return this.request<Employee>("POST", "/employees", { name, role, provider: "mock", model: "mock" });
  }
  transitionEmployee(id: string, action: string) {
    return this.request<Employee>("POST", `/employees/${id}/transition`, { action });
  }

  listSkills() { return this.request<Skill[]>("GET", "/skills"); }
  listCourses() { return this.request<Course[]>("GET", "/academy/courses"); }

  runTask(task: string, employeeId = "") {
    return this.request<TaskResult>("POST", "/tasks", { task, employee_id: employeeId });
  }
}
