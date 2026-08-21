export interface Employee {
  id: string;
  name: string;
  role: string;
  status: string;
  provider: string;
  model: string;
  capabilities: string[];
  skills: string[];
}

export interface Skill {
  id: string;
  name: string;
  version: string;
  description: string;
  category: string;
  tags: string[];
}

export interface Course {
  id: string;
  title: string;
  description: string;
  level: string;
}

export interface TaskResult {
  task: string;
  employee_id: string;
  trace_id: string;
  iterations: number;
  answer: string;
  tool_calls: any[];
}
