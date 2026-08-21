# 快速开始

## 1. 安装

```bash
git clone https://github.com/huzjie/agentdesk.git
cd agentdesk
pip install -e .            # 核心零依赖
pip install -e ".[api]"     # 可选：控制面（fastapi + uvicorn）
```

## 2. 自检

```bash
agentdesk doctor
```

输出类似：

```json
{
  "version": "1.0.0",
  "provider": "mock",
  "model": "mock",
  "workspace": "~/.agentdesk/workspace",
  "sandbox": "subprocess",
  "computer_mode": "mock",
  "employees": 0,
  "skills": 0,
  "courses": 3,
  "tools": 5
}
```

## 3. 第一个数字员工

```bash
agentdesk skill load
agentdesk employee create --name Alice --role analyst
agentdesk employee onboard --id <返回的 employee_id>
agentdesk employee list
```

## 4. 跑任务

```bash
agentdesk task "write a report file"
```

mock provider 会调用 `write_file` 工具，在工作区生成 `report.md`。

## 5. 启动控制面

```bash
agentdesk serve --host 0.0.0.0 --port 8500
# OpenAPI: http://127.0.0.1:8500/docs
# 指标:    http://127.0.0.1:8500/metrics
```

## 6. 前端控制台

```bash
cd console
npm install
npm run dev
```

打开 http://localhost:5173。
