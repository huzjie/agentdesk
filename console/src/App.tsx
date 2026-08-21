import { useEffect, useState } from "react";

const API = "/api";

interface Employee { id: string; name: string; role: string; status: string; provider: string; model: string; }
interface Skill { id: string; name: string; version: string; category: string; }
interface Course { id: string; title: string; level: string; }

export default function App() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [task, setTask] = useState("");
  const [result, setResult] = useState<string>("");

  const refresh = async () => {
    try {
      const [e, s, c] = await Promise.all([
        fetch(API + "/employees").then((r) => r.json()),
        fetch(API + "/skills").then((r) => r.json()),
        fetch(API + "/academy/courses").then((r) => r.json()),
      ]);
      setEmployees(e); setSkills(s); setCourses(c);
    } catch (err) {
      setResult("无法连接控制面，请确认 `agentdesk serve` 已启动");
    }
  };

  useEffect(() => { refresh(); }, []);

  const runTask = async () => {
    const res = await fetch(API + "/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task, employee_id: "" }),
    });
    setResult(JSON.stringify(await res.json(), null, 2));
  };

  return (
    <div className="app">
      <header className="topbar">
        <h1>AgentDesk <span>数字员工运营平台</span></h1>
        <button onClick={refresh}>刷新</button>
      </header>

      <div className="grid">
        <section className="card">
          <h2>数字员工 <em>{employees.length}</em></h2>
          <table>
            <thead><tr><th>名称</th><th>角色</th><th>状态</th><th>Provider</th></tr></thead>
            <tbody>
              {employees.map((e) => (
                <tr key={e.id}>
                  <td>{e.name}</td><td>{e.role}</td>
                  <td><span className={"status " + e.status}>{e.status}</span></td>
                  <td>{e.provider}/{e.model}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="card">
          <h2>技能库 <em>{skills.length}</em></h2>
          <ul>
            {skills.map((s) => (
              <li key={s.id}>{s.name} <code>@{s.version}</code> <span className="dim">[{s.category}]</span></li>
            ))}
          </ul>
        </section>

        <section className="card">
          <h2>课程 <em>{courses.length}</em></h2>
          <ul>
            {courses.map((c) => (
              <li key={c.id}>{c.title} <span className="dim">[{c.level}]</span></li>
            ))}
          </ul>
        </section>

        <section className="card">
          <h2>任务执行</h2>
          <textarea value={task} onChange={(e) => setTask(e.target.value)}
            placeholder="例如：写一份报告 / 列出文件 / echo 测试" />
          <button onClick={runTask}>运行</button>
          {result && <pre>{result}</pre>}
        </section>
      </div>
    </div>
  );
}
