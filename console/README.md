# AgentDesk Console

React 18 + Vite dashboard for the AgentDesk control plane.

```bash
cd console
npm install
npm run dev     # dev server on :5173, proxies /api -> :8500
npm run build   # production build to dist/
```

The control plane must be running (`agentdesk serve`) for the console to
display live data.
